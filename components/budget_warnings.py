"""
Budget Warning Component for Agentic Travel Planner
Implements budget threshold warnings with suggested minimum budgets
"""

from typing import Dict, Any, Optional


class BudgetWarningSystem:
    """Manages budget warnings and recommendations"""
    
    def __init__(self):
        self.warning_thresholds = {
            "very_low": 30,  # USD equivalent
            "low": 50,       # USD equivalent
            "adequate": 100  # USD equivalent
        }
        
        self.currency_rates = {
            "INR": 0.012,
            "USD": 1.0,
            "EUR": 1.08,
            "GBP": 1.25,
            "JPY": 0.0067,
            "CAD": 0.74,
            "AUD": 0.65,
            "SGD": 0.75,
            "CNY": 0.14
        }
    
    def convert_to_usd(self, amount: float, currency: str) -> float:
        """Convert amount to USD"""
        rate = self.currency_rates.get(currency.upper(), 1.0)
        return amount * rate
    
    def convert_from_usd(self, usd_amount: float, currency: str) -> float:
        """Convert USD amount to specified currency"""
        rate = self.currency_rates.get(currency.upper(), 1.0)
        return usd_amount / rate
    
    def calculate_suggested_minimum(self, daily_usd: float, currency: str) -> float:
        """Calculate suggested minimum budget"""
        if daily_usd < self.warning_thresholds["very_low"]:
            # Suggest 2x for very low budgets
            suggested_usd = daily_usd * 2.0
        elif daily_usd < self.warning_thresholds["low"]:
            # Suggest 1.5x for low budgets
            suggested_usd = daily_usd * 1.5
        else:
            # No suggestion needed for adequate budgets
            return None
        
        return round(self.convert_from_usd(suggested_usd, currency), 2)
    
    def get_budget_warning(self, daily_budget: float, currency: str) -> Optional[Dict[str, Any]]:
        """Get budget warning based on daily budget"""
        daily_usd = self.convert_to_usd(daily_budget, currency)
        
        if daily_usd < self.warning_thresholds["very_low"]:
            suggested = self.calculate_suggested_minimum(daily_usd, currency)
            return {
                "level": "critical",
                "message": "Your daily budget is extremely low for this destination. Significant compromises will be required.",
                "suggested_minimum": suggested,
                "suggested_action": "Consider increasing your budget by 100% or choosing a more affordable destination",
                "risk_level": "high"
            }
        elif daily_usd < self.warning_thresholds["low"]:
            suggested = self.calculate_suggested_minimum(daily_usd, currency)
            return {
                "level": "warning",
                "message": "Your daily budget is below the typical minimum for this destination.",
                "suggested_minimum": suggested,
                "suggested_action": "Consider increasing your budget by 50% or adjusting your expectations",
                "risk_level": "medium"
            }
        elif daily_usd < self.warning_thresholds["adequate"]:
            return {
                "level": "info",
                "message": "Your budget is adequate but requires careful planning.",
                "suggested_action": "Prioritize spending on what matters most to you",
                "risk_level": "low"
            }
        else:
            return {
                "level": "success",
                "message": "Your budget is sufficient for a comfortable travel experience.",
                "suggested_action": "Consider upgrading some categories for a better experience",
                "risk_level": "low"
            }
    
    def get_budget_risk_color(self, risk_level: str) -> str:
        """Get color code for budget risk level"""
        colors = {
            "critical": "#EF4444",
            "high": "#EF4444",
            "medium": "#F59E0B",
            "low": "#10B981",
            "success": "#10B981"
        }
        return colors.get(risk_level.lower(), "#6B7280")
    
    def get_budget_risk_label(self, risk_level: str) -> str:
        """Get label for budget risk level"""
        labels = {
            "critical": "CRITICAL",
            "high": "HIGH",
            "medium": "MEDIUM",
            "low": "LOW",
            "success": "LOW"
        }
        return labels.get(risk_level.lower(), "UNKNOWN")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "warning_thresholds": self.warning_thresholds,
            "currency_rates": self.currency_rates
        }


# Initialize budget warning system
budget_warning_system = BudgetWarningSystem()
