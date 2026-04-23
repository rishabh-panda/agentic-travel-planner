from typing import Dict, Any
from models.cost_constants import QUALITY_THRESHOLDS


class QualityChecker:
    
    def assess_quality_risk(self, destination: str, daily_budget_usd: float, 
                            traveller_type: str, user_currency: str = "USD",
                            daily_budget_user: float = None) -> Dict[str, Any]:
        
        thresholds = QUALITY_THRESHOLDS.get(traveller_type, QUALITY_THRESHOLDS["mid-range"])
        budget_for_comparison = daily_budget_usd
        
        if budget_for_comparison < thresholds["warning_threshold"]:
            risk_level = "critical"
            message = f"Daily budget of {self._format_currency(daily_budget_user, user_currency) if daily_budget_user else f'{daily_budget_usd:.2f} USD'} is extremely low for {destination}. Expect significant compromises in quality, safety, or comfort."
            suggested_action = f"Increase daily budget by at least {int((thresholds['min_daily_usd'] / budget_for_comparison - 1) * 100)}% or choose a more affordable destination"
        elif budget_for_comparison < thresholds["min_daily_usd"]:
            risk_level = "high"
            message = f"Budget is below typical minimum for {traveller_type} travel in {destination}. You may face uncomfortable accommodations or limited options."
            suggested_action = f"Increase daily budget by {int((thresholds['min_daily_usd'] / budget_for_comparison - 1) * 100)}% or adjust expectations downward"
        elif budget_for_comparison > thresholds["max_daily_usd"]:
            risk_level = "low"
            message = f"Budget is sufficient for comfortable {traveller_type} travel in {destination}"
            suggested_action = "Consider upgrading some categories for better experience"
        else:
            risk_level = "medium"
            message = f"Budget is adequate for {traveller_type} travel in {destination} but requires careful planning"
            suggested_action = "Prioritize spending on what matters most to you"
        
        return {
            "risk_level": risk_level,
            "message": message,
            "suggested_action": suggested_action,
            "daily_budget_usd": round(daily_budget_usd, 2),
            "thresholds": thresholds
        }
    
    def _format_currency(self, amount: float, currency: str) -> str:
        if amount is None:
            return "Unknown"
        
        symbols = {
            "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥",
            "INR": "₹", "CNY": "¥", "SGD": "S$", "CAD": "C$", "AUD": "A$"
        }
        symbol = symbols.get(currency.upper(), currency)
        return f"{symbol}{amount:.2f}"