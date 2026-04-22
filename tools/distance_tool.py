from typing import Dict, Any
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time


def calculate_travel_time(origin: str, destination: str, mode: str = "walking") -> Dict[str, Any]:
    """
    Calculate approximate travel time between two locations.
    
    Args:
        origin (str): Starting location.
        destination (str): Destination location.
        mode (str): 'walking', 'driving', or 'transit'.
    
    Returns:
        Dict[str, Any]: Travel time and distance.
    """
    try:
        geolocator = Nominatim(user_agent="travel_planner")
        
        origin_location = geolocator.geocode(origin, timeout=10)
        dest_location = geolocator.geocode(destination, timeout=10)
        
        if not origin_location or not dest_location:
            return _get_fallback_travel_time(origin, destination, mode)
        
        origin_coords = (origin_location.latitude, origin_location.longitude)
        dest_coords = (dest_location.latitude, dest_location.longitude)
        
        distance_km = geodesic(origin_coords, dest_coords).kilometers
        
        speeds = {
            "walking": 5,
            "driving": 50,
            "transit": 30
        }
        
        speed_kmh = speeds.get(mode, 30)
        hours = distance_km / speed_kmh
        minutes = round(hours * 60)
        
        return {
            "origin": origin,
            "destination": destination,
            "distance_km": round(distance_km, 1),
            "mode": mode,
            "travel_time_minutes": minutes,
            "travel_time_text": f"{minutes} minutes" if minutes < 60 else f"{minutes // 60} hours {minutes % 60} minutes",
            "source": "OpenStreetMap (free)"
        }
    
    except Exception as e:
        print(f"Distance calculation error: {e}")
        return _get_fallback_travel_time(origin, destination, mode)


def _get_fallback_travel_time(origin: str, destination: str, mode: str) -> Dict[str, Any]:
    """Provide fallback travel time estimates."""
    return {
        "origin": origin,
        "destination": destination,
        "distance_km": 5.0,
        "mode": mode,
        "travel_time_minutes": 30,
        "travel_time_text": "30 minutes",
        "source": "Fallback estimate",
        "warning": "Using approximate travel time"
    }