from typing import Dict, List, Any
import json
import os


class CostAnalyzer:
    """Analyzes destination-specific costs and provides adjustments."""
    
    def __init__(self, data_path: str = "data/destination_costs.json"):
        self.data_path = data_path
        self.destination_costs = self._load_destination_costs()
    
    def _load_destination_costs(self) -> Dict[str, Any]:
        """Load destination cost data from JSON file."""
        default_costs = {
            "default": {
                "budget": {"daily_min": 50, "daily_avg": 80, "daily_max": 120},
                "mid-range": {"daily_min": 80, "daily_avg": 120, "daily_max": 200},
                "luxury": {"daily_min": 200, "daily_avg": 300, "daily_max": 500}
            }
        }
        
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading destination costs: {e}")
                return default_costs
        
        return default_costs
    
    def get_destination_costs(self, destination: str, traveller_type: str) -> Dict[str, float]:
        """Get cost estimates for a specific destination."""
        dest_key = self._normalize_destination(destination)
        
        if dest_key in self.destination_costs:
            costs = self.destination_costs[dest_key].get(traveller_type, self.destination_costs["default"][traveller_type])
        else:
            costs = self.destination_costs["default"][traveller_type]
        
        return costs
    
    def get_cost_adjustments(self, destination: str, traveller_type: str) -> Dict[str, float]:
        """Get category-specific cost adjustments for destination."""
        from models.cost_constants import DESTINATION_COST_MULTIPLIERS
        
        region = self._detect_region(destination)
        multiplier = DESTINATION_COST_MULTIPLIERS.get(region, 1.0)
        
        adjustments = {
            "accommodation": multiplier,
            "food": multiplier,
            "activities": multiplier,
            "transport": multiplier,
            "misc": multiplier
        }
        
        return adjustments
    
    def _normalize_destination(self, destination: str) -> str:
        """Normalize destination name for lookup."""
        return destination.lower().strip().replace(" ", "_")
    
    def _detect_region(self, destination: str) -> str:
        """Detect region from destination name."""
        region_keywords = {
            "Western Europe": ["france", "germany", "italy", "spain", "uk", "united kingdom", "netherlands", "switzerland", "austria"],
            "North America": ["usa", "united states", "canada", "mexico"],
            "Southeast Asia": ["thailand", "vietnam", "indonesia", "malaysia", "philippines", "singapore", "cambodia"],
            "South Asia": ["india", "sri lanka", "nepal", "bangladesh", "pakistan"],
            "Japan": ["japan"],
            "Eastern Europe": ["poland", "hungary", "czech", "croatia", "romania", "bulgaria"],
            "South America": ["brazil", "argentina", "peru", "chile", "colombia"],
            "Australia": ["australia", "new zealand"],
            "Africa": ["south africa", "kenya", "morocco", "egypt", "tanzania"],
            "Middle East": ["uae", "dubai", "qatar", "saudi", "oman", "jordan", "israel"]
        }
        
        dest_lower = destination.lower()
        for region, keywords in region_keywords.items():
            if any(keyword in dest_lower for keyword in keywords):
                return region
        
        return "South Asia"  # Default to lower-cost region if unknown