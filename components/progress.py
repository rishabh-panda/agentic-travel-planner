"""
Progress Indicator Component for Agentic Travel Planner
Implements loading state and progress feedback for multi-agent generation
"""

from typing import Dict, Any, Optional
from datetime import datetime


class ProgressState:
    """Progress tracking for multi-agent generation"""
    RESEARCH_AGENT = 25
    BUDGET_AGENT = 50
    LOGISTICS_AGENT = 75
    SUMMARISER_AGENT = 90
    COMPLETE = 100
    
    AGENT_NAMES = {
        RESEARCH_AGENT: "Research Agent",
        BUDGET_AGENT: "Budget Agent", 
        LOGISTICS_AGENT: "Logistics Agent",
        SUMMARISER_AGENT: "Summariser Agent"
    }
    
    AGENT_DESCRIPTIONS = {
        RESEARCH_AGENT: "Finding attractions and weather information...",
        BUDGET_AGENT: "Calculating budget breakdown...",
        LOGISTICS_AGENT: "Creating day-by-day itinerary...",
        SUMMARISER_AGENT: "Generating final itinerary summary...",
        COMPLETE: "Complete!"
    }


class ProgressIndicator:
    """Manages progress tracking and display for travel plan generation"""
    
    def __init__(self):
        self.current_progress = 0
        self.current_agent = None
        self.start_time = None
        self.estimated_time = 25  # seconds
        self.warning_shown = False
    
    def start_generation(self) -> Dict[str, Any]:
        """Initialize progress tracking for new generation"""
        self.current_progress = 0
        self.current_agent = None
        self.start_time = datetime.now()
        self.warning_shown = False
        
        return self.get_progress_state()
    
    def update_progress(self, step: int, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """Update progress to specified step"""
        self.current_progress = step
        self.current_agent = agent_name
        
        return self.get_progress_state()
    
    def get_progress_state(self) -> Dict[str, Any]:
        """Get current progress state"""
        elapsed = 0
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
        
        remaining = max(0, self.estimated_time - elapsed)
        
        return {
            "progress": self.current_progress,
            "agent_name": self.current_agent,
            "agent_description": ProgressState.AGENT_DESCRIPTIONS.get(
                self.current_progress, "Processing..."
            ),
            "elapsed_time": round(elapsed, 1),
            "estimated_time": self.estimated_time,
            "remaining_time": round(remaining, 1),
            "warning_shown": self.warning_shown
        }
    
    def check_45_second_warning(self) -> Dict[str, Any]:
        """Check if 45 second warning should be shown"""
        if not self.start_time:
            return {"should_warn": False}
        
        elapsed = (datetime.now() - self.start_time).total_seconds()
        should_warn = elapsed >= 45 and not self.warning_shown
        
        if should_warn:
            self.warning_shown = True
        
        return {
            "should_warn": should_warn,
            "elapsed_time": round(elapsed, 1),
            "warning_shown": self.warning_shown
        }
    
    def reset(self) -> None:
        """Reset progress tracking"""
        self.__init__()
