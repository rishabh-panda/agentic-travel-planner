"""
Destination Autocomplete Component for Agentic Travel Planner
Provides real-time suggestions based on popular destinations
"""

from typing import Dict, Any, List, Optional
from difflib import get_close_matches


class DestinationAutocomplete:
    """Manages destination autocomplete suggestions"""
    
    def __init__(self):
        # Popular destinations database
        self.destinations = [
            # Asia
            "Tokyo", "Kyoto", "Bangkok", "Singapore", "Hong Kong",
            "Seoul", "Taipei", "Shanghai", "Beijing", "Dubai",
            "Bali", "Phuket", "Manila", "Hanoi", "Ho Chi Minh City",
            "New Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore",
            "Kuala Lumpur", "Jakarta", "Chiang Mai", "Singapore",
            # Europe
            "Paris", "London", "Rome", "Barcelona", "Amsterdam",
            "Berlin", "Vienna", "Prague", "Dublin", "Lisbon",
            "Madrid", "Munich", "Brussels", "Copenhagen", "Stockholm",
            "Oslo", "Helsinki", "Warsaw", "Budapest", "Athens",
            "Istanbul", "Moscow", "Saint Petersburg", "Edinburgh", "Manchester",
            # North America
            "New York", "Los Angeles", "Chicago", "San Francisco", "Las Vegas",
            "Miami", "Seattle", "Denver", "Boston", "Washington",
            "Toronto", "Vancouver", "Montreal", "Mexico City", "Cancun",
            "Orlando", "San Diego", "Dallas", "Houston", "Phoenix",
            # South America
            "Rio de Janeiro", "Sao Paulo", "Buenos Aires", "Santiago", "Lima",
            "Bogota", "Cusco", "Mendoza", "Cartagena", "San Juan",
            # Africa
            "Cairo", "Cape Town", "Johannesburg", "Marrakech", "Nairobi",
            "Zanzibar", "Luxor", "Tunis", "Tangier", "Dakhla",
            # Oceania
            "Sydney", "Melbourne", "Brisbane", "Auckland", "Wellington",
            "Queenstown", "Fiji", "Bora Bora", "Tahiti", "Nadi"
        ]
    
    def get_suggestions(self, query: str, max_results: int = 5) -> List[str]:
        """Get autocomplete suggestions for query"""
        if not query or len(query) < 2:
            return []
        
        query_lower = query.lower()
        
        # Filter destinations that start with or contain the query
        matches = []
        for dest in self.destinations:
            if dest.lower().startswith(query_lower):
                matches.append(dest)
        
        # If not enough matches, use fuzzy matching
        if len(matches) < max_results:
            fuzzy_matches = get_close_matches(
                query_lower,
                [d.lower() for d in self.destinations],
                n=max_results - len(matches),
                cutoff=0.3
            )
            for match in fuzzy_matches:
                if match.capitalize() not in matches:
                    matches.append(match.capitalize())
        
        return matches[:max_results]
    
    def get_popular_destinations(self, count: int = 10) -> List[str]:
        """Get popular destinations"""
        return self.destinations[:count]
    
    def get_destinations_by_region(self, region: str) -> List[str]:
        """Get destinations by region"""
        regions = {
            "asia": ["Tokyo", "Kyoto", "Bangkok", "Singapore", "Hong Kong",
                    "Seoul", "Taipei", "Shanghai", "Beijing", "Dubai",
                    "Bali", "Phuket", "Manila", "Hanoi", "Ho Chi Minh City",
                    "New Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore",
                    "Kuala Lumpur", "Jakarta", "Chiang Mai"],
            "europe": ["Paris", "London", "Rome", "Barcelona", "Amsterdam",
                      "Berlin", "Vienna", "Prague", "Dublin", "Lisbon",
                      "Madrid", "Munich", "Brussels", "Copenhagen", "Stockholm",
                      "Oslo", "Helsinki", "Warsaw", "Budapest", "Athens",
                      "Istanbul", "Moscow", "Saint Petersburg"],
            "north_america": ["New York", "Los Angeles", "Chicago", "San Francisco", "Las Vegas",
                             "Miami", "Seattle", "Denver", "Boston", "Washington",
                             "Toronto", "Vancouver", "Montreal", "Mexico City", "Cancun"],
            "south_america": ["Rio de Janeiro", "Sao Paulo", "Buenos Aires", "Santiago", "Lima",
                             "Bogota", "Cusco", "Mendoza", "Cartagena", "San Juan"],
            "africa": ["Cairo", "Cape Town", "Johannesburg", "Marrakech", "Nairobi",
                      "Zanzibar", "Luxor", "Tunis", "Tangier", "Dakhla"],
            "oceania": ["Sydney", "Melbourne", "Brisbane", "Auckland", "Wellington",
                       "Queenstown", "Fiji", "Bora Bora", "Tahiti", "Nadi"]
        }
        
        return regions.get(region.lower(), [])
    
    def validate_destination(self, destination: str) -> bool:
        """Check if destination exists in database"""
        return destination.lower() in [d.lower() for d in self.destinations]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "destinations": self.destinations,
            "destination_count": len(self.destinations)
        }


# Initialize destination autocomplete
destination_autocomplete = DestinationAutocomplete()
