"""
Warning System Component for Agentic Travel Planner
Implements 45-second warning and other user notifications
"""

from typing import Dict, Any, Optional
from datetime import datetime


class WarningSystem:
    """Manages warnings and alerts for the application"""
    
    def __init__(self):
        self.warnings = []
        self.warning_thresholds = {
            "generation_timeout": 45,  # seconds
            "low_budget_warning": 30,  # USD equivalent
            "very_low_budget_warning": 50  # USD equivalent
        }
        self.warning_types = {
            "timeout": "timeout",
            "low_budget": "low_budget",
            "very_low_budget": "very_low_budget",
            "date_range": "date_range",
            "min_length": "min_length"
        }
    
    def check_generation_timeout(self, start_time: datetime) -> Dict[str, Any]:
        """Check if generation has exceeded timeout threshold"""
        elapsed = (datetime.now() - start_time).total_seconds()
        should_warn = elapsed >= self.warning_thresholds["generation_timeout"]
        
        return {
            "should_warn": should_warn,
            "elapsed_time": round(elapsed, 1),
            "threshold": self.warning_thresholds["generation_timeout"],
            "warning_type": self.warning_types["timeout"],
            "message": "Generation is taking longer than expected. You can cancel and try again.",
            "action": "cancel"
        }
    
    def check_budget_warning(self, daily_budget: float, currency: str) -> Optional[Dict[str, Any]]:
        """Check if budget is too low for destination"""
        # Convert to USD for threshold comparison
        usd_rates = {"INR": 0.012, "USD": 1.0, "EUR": 1.08, "GBP": 1.25}
        rate = usd_rates.get(currency.upper(), 1.0)
        daily_usd = daily_budget * rate
        
        if daily_usd < self.warning_thresholds["very_low_budget_warning"]:
            return {
                "warning_type": self.warning_types["very_low_budget"],
                "message": "Your daily budget appears very low for this destination.",
                "suggested_minimum": self._calculate_suggested_budget(daily_usd, currency),
                "action": "increase_budget"
            }
        elif daily_usd < self.warning_thresholds["low_budget_warning"]:
            return {
                "warning_type": self.warning_types["low_budget"],
                "message": "Your daily budget is below typical minimum.",
                "suggested_minimum": self._calculate_suggested_budget(daily_usd, currency),
                "action": "consider_increase"
            }
        return None
    
    def _calculate_suggested_budget(self, daily_usd: float, currency: str) -> float:
        """Calculate suggested minimum budget"""
        usd_rates = {"INR": 0.012, "USD": 1.0, "EUR": 1.08, "GBP": 1.25}
        rate = usd_rates.get(currency.upper(), 1.0)
        
        # Suggest at least 2x current budget for very low, 1.5x for low
        if daily_usd < 30:
            suggested_usd = daily_usd * 2.0
        else:
            suggested_usd = daily_usd * 1.5
        
        return round(suggested_usd / rate, 2)
    
    def check_date_range_warning(self, days: int, budget: float) -> Optional[Dict[str, Any]]:
        """Check if date range is invalid"""
        if days <= 0:
            return {
                "warning_type": self.warning_types["date_range"],
                "message": "Number of days must be at least 1",
                "action": "fix_input"
            }
        if budget <= 0:
            return {
                "warning_type": self.warning_types["date_range"],
                "message": "Budget must be greater than 0",
                "action": "fix_input"
            }
        if days > 365:
            return {
                "warning_type": self.warning_types["date_range"],
                "message": "Trip duration cannot exceed 365 days",
                "action": "fix_input"
            }
        return None
    
    def check_min_length_warning(self, text: str, min_length: int = 3) -> Optional[Dict[str, Any]]:
        """Check if text meets minimum length requirement"""
        if len(text) < min_length:
            return {
                "warning_type": self.warning_types["min_length"],
                "message": f"Please enter at least {min_length} characters",
                "current_length": len(text),
                "min_length": min_length,
                "action": "add_more_text"
            }
        return None
    
    def add_warning(self, warning_type: str, message: str, action: str = None) -> None:
        """Add a warning to the list"""
        self.warnings.append({
            "warning_type": warning_type,
            "message": message,
            "action": action,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_warnings(self) -> list:
        """Get all warnings"""
        return self.warnings
    
    def clear_warnings(self) -> None:
        """Clear all warnings"""
        self.warnings = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "warnings": self.warnings,
            "warning_thresholds": self.warning_thresholds
        }
