"""
Property Tests for Input Validation Feedback
Validates: Requirements 4.1, 4.2, 4.3
"""

import pytest
from components.validation import InputValidator
from components.budget_warnings import BudgetWarningSystem
from components.date_validation import DateRangeValidator


class TestInputValidationFeedback:
    """Property tests for input validation feedback"""
    
    @pytest.mark.property_test
    def test_minimum_length_validation_for_destination(self):
        """
        Property: Input Validation Feedback
        
        For any destination input, the system shall validate minimum length (3 characters)
        """
        validator = InputValidator()
        
        # Test with empty string
        valid, error = validator.validate_destination("")
        assert valid is False, "Expected validation to fail for empty destination"
        assert error is not None, "Expected error message for empty destination"
        
        # Test with 1 character
        valid, error = validator.validate_destination("a")
        assert valid is False, "Expected validation to fail for 1 character"
        assert error is not None, "Expected error message for 1 character"
        assert "at least 3 characters" in error.lower(), \
            f"Expected 'at least 3 characters' in error, got '{error}'"
        
        # Test with 2 characters
        valid, error = validator.validate_destination("ab")
        assert valid is False, "Expected validation to fail for 2 characters"
        assert error is not None, "Expected error message for 2 characters"
        assert "at least 3 characters" in error.lower(), \
            f"Expected 'at least 3 characters' in error, got '{error}'"
        
        # Test with exactly 3 characters
        valid, error = validator.validate_destination("abc")
        assert valid is True, \
            f"Expected validation to pass for 'abc', but it failed"
        assert error is None, \
            f"Expected no error for 'abc', but got '{error}'"
        
        # Test with more than 3 characters
        valid, error = validator.validate_destination("abcd")
        assert valid is True, \
            f"Expected validation to pass for 'abcd', but it failed"
    
    @pytest.mark.property_test
    def test_budget_threshold_warnings_with_suggested_minimum(self):
        """
        Property: Input Validation Feedback
        
        For any budget input, the system shall display appropriate warnings with suggested minimum
        """
        warning_system = BudgetWarningSystem()
        
        # Test very low budget (INR)
        warning = warning_system.get_budget_warning(500, "INR")  # ~6 USD
        assert warning is not None, "Expected warning for very low budget"
        assert warning["level"] == "critical", \
            f"Expected critical level, got '{warning['level']}'"
        assert warning["suggested_minimum"] is not None, \
            "Expected suggested minimum for very low budget"
        assert warning["suggested_action"] is not None, \
            "Expected suggested action for very low budget"
        
        # Test low budget (INR) - around 24 USD
        warning = warning_system.get_budget_warning(2000, "INR")
        assert warning is not None, "Expected warning for low budget"
        # Note: 2000 INR = ~24 USD, which is below 30 USD threshold (critical)
        # This is expected behavior - the threshold is 30 USD for critical
        assert warning["level"] in ["critical", "warning"], \
            f"Expected critical or warning level, got '{warning['level']}'"
        assert warning["suggested_minimum"] is not None, \
            "Expected suggested minimum for low budget"
        
        # Test adequate budget (INR) - around 120 USD
        warning = warning_system.get_budget_warning(10000, "INR")
        assert warning is not None, "Expected warning for adequate budget"
        # Note: 10000 INR = ~120 USD, which is above 100 USD threshold (adequate)
        # This is expected behavior - the threshold is 100 USD for adequate
        assert warning["level"] in ["info", "success"], \
            f"Expected info or success level, got '{warning['level']}'"
        assert warning["suggested_action"] is not None, \
            "Expected suggested action for adequate budget"
        
        # Test high budget (INR) - around 600 USD
        warning = warning_system.get_budget_warning(50000, "INR")
        assert warning is not None, "Expected warning for high budget"
        assert warning["level"] == "success", \
            f"Expected success level, got '{warning['level']}'"
    
    @pytest.mark.property_test
    def test_date_range_validation_prevents_invalid_submissions(self):
        """
        Property: Input Validation Feedback
        
        For any date range input, the system shall prevent invalid submissions
        """
        validator = DateRangeValidator()
        
        # Test invalid days (0)
        valid, errors = validator.validate_date_range(0, 1000)
        assert valid is False, "Expected validation to fail for 0 days"
        assert len(errors) > 0, "Expected errors for 0 days"
        assert any(e["field"] == "days" for e in errors), \
            "Expected days field error for 0 days"
        
        # Test invalid days (negative)
        valid, errors = validator.validate_date_range(-5, 1000)
        assert valid is False, "Expected validation to fail for negative days"
        
        # Test invalid days (too many)
        valid, errors = validator.validate_date_range(400, 1000)
        assert valid is False, "Expected validation to fail for 400 days"
        assert any("exceeds" in e["message"].lower() or "cannot exceed" in e["message"].lower() for e in errors), \
            f"Expected 'exceeds' or 'cannot exceed' in error message for 400 days, got: {errors}"
        
        # Test invalid budget (0)
        valid, errors = validator.validate_date_range(3, 0)
        assert valid is False, "Expected validation to fail for 0 budget"
        assert any(e["field"] == "budget" for e in errors), \
            "Expected budget field error for 0 budget"
        
        # Test invalid budget (negative)
        valid, errors = validator.validate_date_range(3, -100)
        assert valid is False, "Expected validation to fail for negative budget"
        
        # Test valid range
        valid, errors = validator.validate_date_range(3, 1000)
        assert valid is True, \
            f"Expected validation to pass for valid range, but got errors: {errors}"
    
    @pytest.mark.property_test
    def test_validation_provides_clear_error_messages(self):
        """
        Property: Input Validation Feedback
        
        For any invalid input, the system shall provide clear error messages
        """
        validator = InputValidator()
        
        # Test destination validation error message
        valid, error = validator.validate_destination("ab")
        assert error is not None, "Expected error message for short destination"
        assert "at least 3 characters" in error.lower(), \
            f"Expected 'at least 3 characters' in error, got '{error}'"
        
        # Test days validation error message
        valid, error = validator.validate_days(0)
        assert error is not None, "Expected error message for 0 days"
        assert "at least 1 day" in error.lower(), \
            f"Expected 'at least 1 day' in error, got '{error}'"
        
        # Test budget validation error message
        valid, error = validator.validate_budget(0)
        assert error is not None, "Expected error message for 0 budget"
        assert "greater than" in error.lower(), \
            f"Expected 'greater than' in error, got '{error}'"
    
    @pytest.mark.property_test
    def test_validation_handles_edge_cases(self):
        """
        Property: Input Validation Feedback
        
        For any edge case, the system shall handle gracefully
        """
        validator = InputValidator()
        
        # Test with None values
        valid, error = validator.validate_destination(None)
        assert valid is False, "Expected validation to fail for None destination"
        
        valid, error = validator.validate_days(None)
        assert valid is False, "Expected validation to fail for None days"
        
        valid, error = validator.validate_budget(None)
        assert valid is False, "Expected validation to fail for None budget"
        
        # Test with empty string
        valid, error = validator.validate_destination("")
        assert valid is False, "Expected validation to fail for empty destination"
        
        # Test with very long strings
        valid, error = validator.validate_destination("a" * 200)
        assert valid is False, "Expected validation to fail for very long destination"
        assert error is not None, "Expected error for very long destination"
    
    @pytest.mark.property_test
    def test_budget_warning_currency_conversion(self):
        """
        Property: Input Validation Feedback
        
        For any currency, the system shall correctly convert to USD for threshold comparison
        """
        warning_system = BudgetWarningSystem()
        
        # Test INR conversion
        usd = warning_system.convert_to_usd(1000, "INR")
        assert 10 < usd < 15, f"Expected USD ~12, got {usd}"
        
        # Test EUR conversion
        usd = warning_system.convert_to_usd(100, "EUR")
        assert 100 < usd < 110, f"Expected USD ~108, got {usd}"
        
        # Test GBP conversion
        usd = warning_system.convert_to_usd(100, "GBP")
        assert 120 < usd < 130, f"Expected USD ~125, got {usd}"
        
        # Test USD conversion
        usd = warning_system.convert_to_usd(100, "USD")
        assert usd == 100, f"Expected USD 100, got {usd}"
    
    @pytest.mark.property_test
    def test_budget_warning_suggested_minimum_calculation(self):
        """
        Property: Input Validation Feedback
        
        For any low budget, the system shall calculate appropriate suggested minimum
        """
        warning_system = BudgetWarningSystem()
        
        # Test very low budget (INR 500 = ~6 USD)
        suggested = warning_system.calculate_suggested_minimum(6, "INR")
        assert suggested is not None, "Expected suggested minimum for very low budget"
        assert suggested > 500, f"Expected suggested > 500 INR, got {suggested}"
        
        # Test low budget (INR 2000 = ~24 USD)
        suggested = warning_system.calculate_suggested_minimum(24, "INR")
        assert suggested is not None, "Expected suggested minimum for low budget"
        assert suggested > 2000, f"Expected suggested > 2000 INR, got {suggested}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
