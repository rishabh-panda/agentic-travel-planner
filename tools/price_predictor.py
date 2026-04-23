from typing import Dict, Any
from datetime import datetime


class PricePredictor:
    """Predicts price surges and recommends optimal booking times."""
    
    def assess_surge_risk(self, destination: str, booking_window_days: int) -> Dict[str, Any]:
        """Assess risk of price surge based on booking window."""
        
        if booking_window_days <= 7:
            risk_level = "critical"
            expected_increase = "50-100%"
            message = "Prices are extremely high due to last-minute booking"
        elif booking_window_days <= 14:
            risk_level = "high"
            expected_increase = "30-50%"
            message = "Significant price surge expected. Book within 48 hours."
        elif booking_window_days <= 30:
            risk_level = "medium"
            expected_increase = "10-30%"
            message = "Moderate price increases likely. Book within 2 weeks."
        elif booking_window_days <= 60:
            risk_level = "low"
            expected_increase = "0-10%"
            message = "Optimal booking window. Prices are stable."
        else:
            risk_level = "very_low"
            expected_increase = "0-5%"
            message = "Too early for best prices. Set a price alert."
        
        return {
            "risk_level": risk_level,
            "expected_increase": expected_increase,
            "message": message,
            "booking_window_days": booking_window_days,
            "recommended_action": self._get_recommended_action(risk_level)
        }
    
    def predict_best_booking_time(self, item_type: str, travel_date: datetime) -> Dict[str, Any]:
        """Predict optimal booking window for specific item types."""
        
        days_to_travel = (travel_date - datetime.now()).days
        
        recommendations = {
            "flights": {
                "optimal_window": (60, 120),
                "too_early": 180,
                "too_late": 21
            },
            "hotels": {
                "optimal_window": (30, 90),
                "too_early": 120,
                "too_late": 14
            },
            "attractions": {
                "optimal_window": (7, 30),
                "too_early": 45,
                "too_late": 3
            }
        }
        
        item_rec = recommendations.get(item_type, recommendations["attractions"])
        
        if days_to_travel > item_rec["too_early"]:
            status = "too_early"
            advice = "Too early to book. Set price alerts and wait."
        elif days_to_travel < item_rec["too_late"]:
            status = "too_late"
            advice = "Book immediately. Prices will only increase."
        elif item_rec["optimal_window"][0] <= days_to_travel <= item_rec["optimal_window"][1]:
            status = "optimal"
            advice = "Optimal booking window. Book now for best prices."
        else:
            status = "acceptable"
            advice = "Acceptable to book, but monitor prices."
        
        return {
            "item_type": item_type,
            "days_to_travel": days_to_travel,
            "status": status,
            "advice": advice,
            "optimal_window": f"{item_rec['optimal_window'][0]}-{item_rec['optimal_window'][1]} days before travel"
        }
    
    def _get_recommended_action(self, risk_level: str) -> str:
        """Get recommended action based on risk level."""
        actions = {
            "critical": "Book immediately - prices increasing hourly",
            "high": "Book within 24-48 hours",
            "medium": "Book within 1-2 weeks",
            "low": "Monitor prices but no immediate urgency",
            "very_low": "Set price alerts and wait for deals"
        }
        return actions.get(risk_level, "Monitor prices")