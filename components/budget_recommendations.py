"""
Budget Recommendations Component for Agentic Travel Planner
Implements budget warning recommendations with animated pulse for critical alerts
"""

from typing import Dict, Any, Optional
from components.budget_warnings import BudgetWarningSystem


class BudgetRecommendations:
    """Manages budget recommendations and critical alerts"""
    
    def __init__(self):
        self.warning_system = BudgetWarningSystem()
        self.animation_duration = 1000  # milliseconds for pulse animation
    
    def get_recommendations(
        self,
        daily_budget: float,
        currency: str,
        days: int
    ) -> Dict[str, Any]:
        """
        Get budget recommendations based on daily budget.
        
        Args:
            daily_budget: Daily budget amount
            currency: Currency code
            days: Number of days
        
        Returns:
            Dictionary with recommendations and alert status
        """
        warning = self.warning_system.get_budget_warning(daily_budget, currency)
        
        if not warning:
            return {
                "has_recommendations": False,
                "recommendations": [],
                "alert": None
            }
        
        recommendations = self._generate_recommendations(warning, daily_budget, currency, days)
        
        # Determine if critical alert with animation is needed
        alert = None
        if warning.get("level") in ["critical", "high"]:
            alert = {
                "type": "critical",
                "message": warning.get("message", ""),
                "should_animate": True,
                "animation_duration": self.animation_duration,
                "action_required": True
            }
        elif warning.get("level") == "medium":
            alert = {
                "type": "warning",
                "message": warning.get("message", ""),
                "should_animate": False,
                "action_required": False
            }
        
        return {
            "has_recommendations": True,
            "recommendations": recommendations,
            "alert": alert,
            "warning": warning
        }
    
    def _generate_recommendations(
        self,
        warning: Dict[str, Any],
        daily_budget: float,
        currency: str,
        days: int
    ) -> list:
        """
        Generate specific recommendations based on warning.
        
        Args:
            warning: Budget warning dictionary
            daily_budget: Daily budget amount
            currency: Currency code
            days: Number of days
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        level = warning.get("level", "info")
        
        if level == "critical":
            recommendations.extend([
                f"Consider reducing trip duration from {days} to 2 days to stay within budget",
                f"Look for budget accommodations under {currency} {int(daily_budget * 0.3)} per night",
                "Prioritize free attractions and public transportation",
                "Consider traveling during off-peak season for lower prices"
            ])
        elif level == "warning":
            recommendations.extend([
                f"Look for accommodations under {currency} {int(daily_budget * 0.4)} per night",
                "Use public transportation instead of taxis",
                "Eat at local markets and street food vendors",
                "Book attractions in advance for discounts"
            ])
        elif level == "info":
            recommendations.extend([
                "Consider upgrading to better accommodations for part of your trip",
                "Try some paid attractions and experiences",
                "Allocate some budget for unexpected opportunities"
            ])
        else:  # success
            recommendations.extend([
                "Consider upgrading to premium experiences",
                "Allocate budget for special dining experiences",
                "Don't hesitate to splurge on a memorable activity"
            ])
        
        return recommendations
    
    def get_critical_alert_html(self, alert: Dict[str, Any]) -> str:
        """
        Generate HTML for critical budget alert with animated pulse.
        
        Args:
            alert: Alert information dictionary
        
        Returns:
            HTML string for critical alert
        """
        return f"""
        <div class="critical-budget-alert" style="
            background-color: #FEF2F2;
            border-left: 4px solid #EF4444;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            animation: pulse {alert.get('animation_duration', 1000)}ms infinite;
        ">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">⚠️</span>
                <div>
                    <strong style="color: #DC2626;">Critical Budget Alert:</strong>
                    <p style="margin: 0.25rem 0 0 0; color: #1F2937;">{alert.get('message', '')}</p>
                </div>
            </div>
        </div>
        """
    
    def get_warning_alert_html(self, alert: Dict[str, Any]) -> str:
        """
        Generate HTML for warning budget alert.
        
        Args:
            alert: Alert information dictionary
        
        Returns:
            HTML string for warning alert
        """
        return f"""
        <div class="warning-budget-alert" style="
            background-color: #FEF3C7;
            border-left: 4px solid #F59E0B;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">⚠️</span>
                <div>
                    <strong style="color: #F59E0B;">Budget Warning:</strong>
                    <p style="margin: 0.25rem 0 0 0; color: #1F2937;">{alert.get('message', '')}</p>
                </div>
            </div>
        </div>
        """
    
    def get_recommendations_html(self, recommendations: list) -> str:
        """
        Generate HTML for budget recommendations.
        
        Args:
            recommendations: List of recommendation strings
        
        Returns:
            HTML string for recommendations
        """
        if not recommendations:
            return ""
        
        items_html = ""
        for rec in recommendations:
            items_html += f"<li style='margin: 0.5rem 0;'>{rec}</li>"
        
        return f"""
        <div class="budget-recommendations" style="
            background-color: #F0F9FF;
            border-left: 4px solid #008080;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        ">
            <strong style="color: #1E3A5F;">Budget Recommendations:</strong>
            <ul style="margin: 0.5rem 0; padding-left: 1.5rem;">
                {items_html}
            </ul>
        </div>
        """
    
    def get_css(self) -> str:
        """
        Get CSS for budget alerts and recommendations.
        
        Returns:
            CSS string for styling
        """
        return """
        .critical-budget-alert {
            animation: pulse 1000ms infinite;
        }
        
        .warning-budget-alert {
            animation: fadeIn 0.3s ease;
        }
        
        .budget-recommendations {
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes pulse {
            0%, 100% {
                box-shadow: 0 1px 3px rgba(239, 68, 68, 0.1);
            }
            50% {
                box-shadow: 0 0 0 10px rgba(239, 68, 68, 0.1);
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        """
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "warning_system": self.warning_system.to_dict(),
            "animation_duration": self.animation_duration
        }
