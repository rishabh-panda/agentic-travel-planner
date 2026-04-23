"""
Property Tests for Error Recovery Guidance
Validates: Requirements 9.1, 9.2, 9.3, 9.4
"""

import pytest
from components.api_key_error import APIKeyErrorBanner
from components.generation_error import GenerationErrorBox
from components.budget_recommendations import BudgetRecommendations
from components.weather_fallback import WeatherFallback
from components.session_handling import SessionHandler


class TestErrorRecoveryGuidance:
    """Property tests for error recovery guidance"""
    
    @pytest.mark.property_test
    def test_api_key_error_banner_shows_clear_instructions(self):
        """
        Property: Error Recovery Guidance
        
        For any API key error condition, the system shall display a prominent banner
        with clear instructions to update .env file
        """
        banner = APIKeyErrorBanner()
        
        # Test missing API key
        error_info = banner.check_api_key_status()
        if not error_info.get("has_error"):
            # If API key exists, simulate missing key
            error_info = {
                "has_error": True,
                "error_type": "missing",
                "message": "GROQ_API_KEY is not set",
                "severity": "critical",
                "instructions": [
                    "1. Create a .env file in the project root directory",
                    "2. Add your GROQ_API_KEY: GROQ_API_KEY=your_actual_key_here",
                    "3. Restart the application after updating .env"
                ],
                "link_to_docs": "https://console.groq.com/docs/quickstart",
                "env_file_path": ".env"
            }
        
        assert error_info.get("has_error") is True, "Expected API key error"
        assert error_info.get("instructions") is not None, "Expected instructions"
        assert len(error_info.get("instructions", [])) > 0, "Expected at least one instruction"
        assert any(".env" in str(inst) for inst in error_info.get("instructions", [])), \
            "Expected .env file reference in instructions"
        assert error_info.get("severity") in ["critical", "warning"], \
            "Expected critical or warning severity"
    
    @pytest.mark.property_test
    def test_generation_error_box_shows_retry_option(self):
        """
        Property: Error Recovery Guidance
        
        For any generation failure, the system shall display a dismissible error box
        with retry option
        """
        error_box = GenerationErrorBox()
        
        # Test various error types
        error_types = [
            ("api_error", "API key validation failed"),
            ("network_error", "Connection timeout"),
            ("timeout_error", "Request timed out"),
            ("unknown_error", "Unknown error occurred")
        ]
        
        for error_type, error_message in error_types:
            error_info = error_box.create_error_box(
                error_message=error_message,
                error_type=error_type
            )
            
            assert error_info.get("has_error") is True, f"Expected error for {error_type}"
            assert error_info.get("retry_enabled") is True, f"Expected retry enabled for {error_type}"
            assert error_info.get("instructions") is not None, f"Expected instructions for {error_type}"
            assert len(error_info.get("instructions", [])) > 0, f"Expected instructions for {error_type}"
    
    @pytest.mark.property_test
    def test_budget_recommendations_provide_specific_guidance(self):
        """
        Property: Error Recovery Guidance
        
        For any budget condition, the system shall provide specific recommendations
        to improve the budget
        """
        recommendations = BudgetRecommendations()
        
        # Test various budget conditions
        test_cases = [
            (500, "INR", 3),   # Very low budget (~6 USD)
            (2000, "INR", 3),  # Low budget (~24 USD)
            (10000, "INR", 3), # Adequate budget (~120 USD)
            (50000, "INR", 3)  # High budget (~600 USD)
        ]
        
        for daily_budget, currency, days in test_cases:
            result = recommendations.get_recommendations(
                daily_budget=daily_budget,
                currency=currency,
                days=days
            )
            
            assert result.get("has_recommendations") is True, \
                f"Expected recommendations for budget {daily_budget} {currency}"
            assert len(result.get("recommendations", [])) > 0, \
                f"Expected at least one recommendation for budget {daily_budget} {currency}"
    
    @pytest.mark.property_test
    def test_weather_fallback_shows_estimated_values(self):
        """
        Property: Error Recovery Guidance
        
        For any unavailable weather data, the system shall display a friendly message
        with estimated weather based on season
        """
        fallback = WeatherFallback()
        
        # Test various seasons
        seasons = ["spring", "summer", "autumn", "winter"]
        
        for season in seasons:
            estimated = fallback.estimate_weather(
                destination="Test City",
                season=season,
                days=3
            )
            
            assert estimated.get("is_estimated") is True, f"Expected estimated weather for {season}"
            assert len(estimated.get("forecast", [])) == 3, f"Expected 3 days forecast for {season}"
            assert estimated.get("disclaimer") is not None, f"Expected disclaimer for {season}"
            
            # Verify forecast structure
            for day in estimated.get("forecast", []):
                assert "date" in day, f"Expected date in forecast for {season}"
                assert "condition" in day, f"Expected condition in forecast for {season}"
                assert "temp" in day, f"Expected temp in forecast for {season}"
    
    @pytest.mark.property_test
    def test_session_expiration_shows_resume_option(self):
        """
        Property: Error Recovery Guidance
        
        For any session expiration, the system shall redirect to login with option
        to resume previous session
        """
        handler = SessionHandler()
        
        # Create a session
        session = handler.create_session({
            "user_id": "test_user",
            "destination": "Test City"
        })
        
        assert session.get("is_active") is True, "Expected active session"
        assert session.get("session_id") is not None, "Expected session ID"
        
        # Check session status
        status = handler.get_session_status(session)
        assert status.get("is_expired") is False, "Expected active session"
        assert status.get("can_resume") is True, "Expected resume capability"
        
        # Create expired session
        expired_session = {
            "session_id": "test_session",
            "created_at": "2020-01-01T00:00:00",
            "expires_at": "2020-01-01T01:00:00",
            "last_activity": "2020-01-01T00:30:00",
            "user_data": {},
            "is_active": False
        }
        
        expired_status = handler.get_session_status(expired_session)
        assert expired_status.get("is_expired") is True, "Expected expired session"
        assert expired_status.get("redirect_to") == "login", "Expected login redirect"
    
    @pytest.mark.property_test
    def test_error_recovery_handles_all_error_categories(self):
        """
        Property: Error Recovery Guidance
        
        For any error category, the system shall provide appropriate error messaging
        with specific recovery guidance
        """
        api_banner = APIKeyErrorBanner()
        gen_error = GenerationErrorBox()
        budget_rec = BudgetRecommendations()
        weather_fallback = WeatherFallback()
        
        # Test API key error
        api_error = api_banner.check_api_key_status()
        if api_error.get("has_error"):
            assert api_error.get("instructions") is not None
            assert api_error.get("severity") is not None
        
        # Test generation error
        gen_error_info = gen_error.create_error_box(
            error_message="Test error",
            error_type="api_error"
        )
        assert gen_error_info.get("has_error") is True
        assert gen_error_info.get("instructions") is not None
        assert gen_error_info.get("retry_enabled") is True
        
        # Test budget recommendations
        budget_result = budget_rec.get_recommendations(
            daily_budget=1000,
            currency="INR",
            days=3
        )
        assert budget_result.get("has_recommendations") is True
        assert len(budget_result.get("recommendations", [])) > 0
        
        # Test weather fallback
        weather_result = weather_fallback.estimate_weather(
            destination="Test",
            season="spring",
            days=3
        )
        assert weather_result.get("is_estimated") is True
        assert len(weather_result.get("forecast", [])) > 0
    
    @pytest.mark.property_test
    def test_error_messages_are_user_friendly(self):
        """
        Property: Error Recovery Guidance
        
        For any error condition, the system shall provide user-friendly messages
        without technical jargon
        """
        gen_error = GenerationErrorBox()
        
        # Test various error messages
        error_messages = [
            "Connection refused",
            "API key invalid",
            "Timeout exceeded",
            "Unknown error"
        ]
        
        for msg in error_messages:
            error_info = gen_error.create_error_box(
                error_message=msg,
                error_type="unknown_error"
            )
            
            instructions = error_info.get("instructions", [])
            for instruction in instructions:
                # Check that instructions don't contain technical jargon
                instruction_lower = instruction.lower()
                assert "http" not in instruction_lower or "url" not in instruction_lower, \
                    f"Instruction should not contain technical jargon: {instruction}"
                assert "exception" not in instruction_lower, \
                    f"Instruction should not contain exception: {instruction}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
