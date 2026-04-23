"""
Tooltip System Component for Agentic Travel Planner
Provides guidance and examples for all input fields
"""

from typing import Dict, Any, Optional


class TooltipManager:
    """Manages tooltips for all input fields"""
    
    def __init__(self):
        self.tooltips = {
            "destination": {
                "title": "Destination",
                "description": "Enter any city or region worldwide where you'd like to travel",
                "placeholder": "e.g., Delhi, Copenhagen, Tokyo",
                "examples": ["Paris", "Tokyo", "New York", "London", "Sydney"]
            },
            "days": {
                "title": "Number of Days",
                "description": "Total trip duration in days",
                "min": 1,
                "max": 365,
                "default": 3
            },
            "budget": {
                "title": "Total Budget",
                "description": "Your total trip budget in the selected currency",
                "min": 0.01,
                "max": 1000000,
                "default": 35000.0
            },
            "currency": {
                "title": "Currency",
                "description": "Select your preferred currency for budget display",
                "options": ["INR", "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "SGD", "CNY"]
            },
            "interests": {
                "title": "Interests",
                "description": "Comma-separated list of your interests to personalize your itinerary",
                "placeholder": "e.g., Culture, Food, Adventure, History, Shopping",
                "examples": [
                    "Culture, Food, History",
                    "Adventure, Nature, Photography",
                    "Shopping, Nightlife, Entertainment",
                    "Beaches, Water Sports, Relaxation",
                    "Museums, Art, Architecture"
                ]
            }
        }
    
    def get_tooltip(self, field_name: str) -> Optional[Dict[str, Any]]:
        """Get tooltip for specified field"""
        return self.tooltips.get(field_name)
    
    def get_all_tooltips(self) -> Dict[str, Any]:
        """Get all tooltips"""
        return self.tooltips
    
    def get_example_interests(self) -> list:
        """Get example interests for hover display"""
        return self.tooltips["interests"]["examples"]
    
    def get_destination_examples(self) -> list:
        """Get destination examples"""
        return self.tooltips["destination"]["examples"]
    
    def get_currency_options(self) -> list:
        """Get currency options"""
        return self.tooltips["currency"]["options"]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "tooltips": self.tooltips,
            "example_interests": self.get_example_interests(),
            "destination_examples": self.get_destination_examples(),
            "currency_options": self.get_currency_options()
        }


# Initialize tooltip manager
tooltip_manager = TooltipManager()
