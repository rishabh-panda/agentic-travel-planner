"""
UI Helper Functions for Enterprise Travel Planner
Version: 1.0.0
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def format_currency(amount: float, currency: str) -> str:
    """
    Format currency amount with proper symbol and decimal places.
    
    Args:
        amount: Numeric amount
        currency: 3-letter currency code
    
    Returns:
        Formatted currency string
    """
    try:
        symbols = {
            "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥",
            "INR": "₹", "CNY": "¥", "SGD": "S$", "CAD": "C$",
            "AUD": "A$", "CHF": "Fr", "NZD": "NZ$", "ZAR": "R"
        }
        symbol = symbols.get(currency.upper(), currency)
        return f"{symbol}{amount:,.2f}"
    except Exception:
        return f"{currency} {amount:.2f}"


def calculate_budget_percentages(breakdown: Dict[str, float]) -> Dict[str, float]:
    """
    Calculate percentage breakdown from daily budget amounts.
    
    Args:
        breakdown: Dictionary of category to amount
    
    Returns:
        Dictionary of category to percentage
    """
    try:
        total = sum(breakdown.values())
        if total == 0:
            return {k: 0.0 for k in breakdown.keys()}
        return {k: (v / total) * 100 for k, v in breakdown.items()}
    except Exception:
        return {}


def get_risk_color(risk_level: str) -> str:
    """
    Get color code for budget risk level.
    
    Args:
        risk_level: low, medium, high, critical
    
    Returns:
        Hex color code
    """
    risk_colors = {
        "low": "#10B981",
        "medium": "#F59E0B",
        "high": "#EF4444",
        "critical": "#DC2626"
    }
    return risk_colors.get(risk_level.lower(), "#6B7280")


def truncate_text(text: str, max_length: int = 150) -> str:
    """
    Truncate text to specified length with ellipsis.
    
    Args:
        text: Input text
        max_length: Maximum characters
    
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def validate_budget_alert(daily_budget: float, currency: str) -> Optional[Dict[str, Any]]:
    """
    Generate budget alert based on daily budget and destination context.
    
    Args:
        daily_budget: Daily budget amount
        currency: Currency code
    
    Returns:
        Alert dictionary or None
    """
    try:
        # Convert to USD for threshold comparison
        usd_rates = {"INR": 0.012, "USD": 1.0, "EUR": 1.08, "GBP": 1.25}
        rate = usd_rates.get(currency.upper(), 1.0)
        daily_usd = daily_budget * rate
        
        if daily_usd < 30:
            return {
                "level": "critical",
                "message": "Daily budget is extremely low. Significant compromises required.",
                "action": "Increase budget by 100% or choose a more affordable destination"
            }
        elif daily_usd < 50:
            return {
                "level": "high",
                "message": "Daily budget is below typical minimum. Limited options available.",
                "action": "Increase budget by 50% or adjust expectations downward"
            }
        elif daily_usd < 100:
            return {
                "level": "medium",
                "message": "Budget is adequate but requires careful planning.",
                "action": "Prioritize spending on what matters most"
            }
        else:
            return {
                "level": "low",
                "message": "Budget is sufficient for comfortable travel.",
                "action": "Consider upgrading some categories for better experience"
            }
    except Exception:
        return None


def create_export_filename(destination: str, date: Optional[datetime] = None) -> str:
    """
    Create a standardized filename for itinerary exports.
    
    Args:
        destination: Travel destination
        date: Optional date for filename
    
    Returns:
        Sanitized filename
    """
    if date is None:
        date = datetime.now()
    
    safe_destination = "".join(c for c in destination if c.isalnum() or c in (' ', '-')).strip().replace(' ', '_')
    return f"itinerary_{safe_destination}_{date.strftime('%Y%m%d')}.txt"