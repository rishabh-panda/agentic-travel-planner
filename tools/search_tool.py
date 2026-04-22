from typing import List, Dict, Any
from ddgs import DDGS


def search_attractions(destination: str, limit: int = 10) -> List[Dict[str, str]]:
    """
    Search for attractions in a given destination.
    
    Args:
        destination (str): City or region name.
        limit (int): Maximum number of results.
    
    Returns:
        List[Dict[str, str]]: List of attractions with names and descriptions.
    """
    try:
        query = f"top tourist attractions in {destination} for travelers"
        
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=limit))
        
        attractions = []
        for result in results:
            attractions.append({
                "name": result.get("title", "Unknown"),
                "description": result.get("body", "No description available")[:200],
                "source": result.get("href", "#")
            })
        
        if not attractions:
            return _get_fallback_attractions(destination)
        
        return attractions
    
    except Exception as e:
        print(f"Search error: {e}")
        return _get_fallback_attractions(destination)


def _get_fallback_attractions(destination: str) -> List[Dict[str, str]]:
    """Provide fallback attractions when search fails."""
    return [
        {
            "name": f"Central {destination} City Tour",
            "description": f"Explore the main landmarks and cultural sites of {destination}.",
            "source": "#"
        },
        {
            "name": f"Local Markets of {destination}",
            "description": "Experience authentic local culture and cuisine.",
            "source": "#"
        },
        {
            "name": f"Historical {destination} Museum",
            "description": "Learn about the rich history and heritage.",
            "source": "#"
        }
    ]