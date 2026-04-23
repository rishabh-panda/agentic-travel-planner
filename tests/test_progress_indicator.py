"""
Property Tests for Progress Indicator Accuracy
Validates: Requirements 2.1, 2.2
"""

import pytest
from datetime import datetime, timedelta
from components.progress import ProgressIndicator, ProgressState


class TestProgressIndicatorAccuracy:
    """Property tests for progress indicator accuracy"""
    
    @pytest.mark.property_test
    def test_progress_indicator_shows_correct_agent_stages(self):
        """
        Property: Progress Indicator Accuracy
        
        For any generation request, the system shall display a progress indicator
        that accurately reflects the current agent processing stage
        (Research: 25%, Budget: 50%, Logistics: 75%, Summariser: 90%)
        """
        progress = ProgressIndicator()
        
        # Test all agent stages
        agent_stages = [
            (ProgressState.RESEARCH_AGENT, "Research Agent"),
            (ProgressState.BUDGET_AGENT, "Budget Agent"),
            (ProgressState.LOGISTICS_AGENT, "Logistics Agent"),
            (ProgressState.SUMMARISER_AGENT, "Summariser Agent"),
            (ProgressState.COMPLETE, "Complete!")
        ]
        
        for expected_progress, expected_agent in agent_stages:
            state = progress.update_progress(expected_progress, expected_agent)
            
            assert state["progress"] == expected_progress, \
                f"Expected progress {expected_progress}, got {state['progress']}"
            assert state["agent_name"] == expected_agent, \
                f"Expected agent {expected_agent}, got {state['agent_name']}"
    
    @pytest.mark.property_test
    def test_progress_indicator_shows_correct_agent_descriptions(self):
        """
        Property: Progress Indicator Accuracy
        
        For any generation request, the system shall display correct agent descriptions
        """
        progress = ProgressIndicator()
        
        # Test all agent descriptions
        expected_descriptions = {
            ProgressState.RESEARCH_AGENT: "Finding attractions and weather information...",
            ProgressState.BUDGET_AGENT: "Calculating budget breakdown...",
            ProgressState.LOGISTICS_AGENT: "Creating day-by-day itinerary...",
            ProgressState.SUMMARISER_AGENT: "Generating final itinerary summary...",
            ProgressState.COMPLETE: "Complete!"
        }
        
        for progress_value, expected_description in expected_descriptions.items():
            state = progress.update_progress(progress_value, f"Agent {progress_value}")
            
            assert state["agent_description"] == expected_description, \
                f"Expected description '{expected_description}', got '{state['agent_description']}'"
    
    @pytest.mark.property_test
    def test_progress_indicator_timing_accuracy(self):
        """
        Property: Progress Indicator Accuracy
        
        For any generation request, the system shall accurately track elapsed time
        """
        progress = ProgressIndicator()
        
        # Start generation
        state = progress.start_generation()
        assert state["progress"] == 0
        assert state["estimated_time"] == 25
        
        # Simulate time passing
        progress.start_time = datetime.now() - timedelta(seconds=10)
        state = progress.get_progress_state()
        
        assert state["elapsed_time"] >= 9.9, \
            f"Expected elapsed time >= 9.9s, got {state['elapsed_time']}"
        assert state["elapsed_time"] <= 10.1, \
            f"Expected elapsed time <= 10.1s, got {state['elapsed_time']}"
        assert state["remaining_time"] >= 14.9, \
            f"Expected remaining time >= 14.9s, got {state['remaining_time']}"
        assert state["remaining_time"] <= 15.1, \
            f"Expected remaining time <= 15.1s, got {state['remaining_time']}"
    
    @pytest.mark.property_test
    def test_progress_indicator_warning_system(self):
        """
        Property: Progress Indicator Accuracy
        
        For any generation request exceeding 45 seconds, the system shall show warning
        """
        progress = ProgressIndicator()
        
        # Start generation
        progress.start_generation()
        
        # Simulate time passing beyond 45 seconds
        progress.start_time = datetime.now() - timedelta(seconds=50)
        
        warning = progress.check_45_second_warning()
        
        assert warning["should_warn"] is True, \
            "Expected warning to be shown after 45 seconds"
        assert warning["elapsed_time"] >= 44.9, \
            f"Expected elapsed time >= 44.9s, got {warning['elapsed_time']}"
        assert warning["warning_shown"] is True, \
            "Expected warning_shown to be True"
    
    @pytest.mark.property_test
    def test_progress_indicator_reset_functionality(self):
        """
        Property: Progress Indicator Accuracy
        
        For any generation request, the system shall properly reset progress
        """
        progress = ProgressIndicator()
        
        # Set some progress
        progress.update_progress(50, "Budget Agent")
        progress.start_generation()
        
        # Reset
        progress.reset()
        
        assert progress.current_progress == 0
        assert progress.current_agent is None
        assert progress.start_time is None
        assert progress.warning_shown is False
    
    @pytest.mark.property_test
    def test_progress_indicator_handles_edge_cases(self):
        """
        Property: Progress Indicator Accuracy
        
        For any edge case, the system shall handle gracefully
        """
        progress = ProgressIndicator()
        
        # Test with None values
        state = progress.get_progress_state()
        assert state["progress"] == 0
        assert state["agent_name"] is None
        
        # Test with 0 progress
        state = progress.update_progress(0, None)
        assert state["progress"] == 0
        
        # Test with 100 progress
        state = progress.update_progress(100, "Complete")
        assert state["progress"] == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
