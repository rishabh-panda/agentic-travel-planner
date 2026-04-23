from typing import List, Dict, Any, Union
from ddgs import DDGS


def search_attractions(destination: str, interests: Union[List[str], int] = 10, limit: int = 10) -> List[Dict[str, str]]:
    """
    Search for attractions in a given destination.
    
    Args:
        destination (str): City or region name.
        interests (Union[List[str], int]): Either a list of interests or limit (for backward compatibility).
        limit (int): Maximum number of results (used if interests is not an int).
    
    Returns:
        List[Dict[str, str]]: List of attractions with names and descriptions.
    """
    # Handle case where second parameter is interests list (not limit)
    if isinstance(interests, list):
        # Use default limit
        actual_limit = limit
    elif isinstance(interests, int):
        # Backward compatibility: second param is actually limit
        actual_limit = interests
    else:
        actual_limit = 10
    
    # Cap limit at reasonable number
    actual_limit = min(actual_limit, 20)
    
    try:
        # Build query with interests if provided
        if isinstance(interests, list) and interests:
            interest_str = " ".join(interests[:3])  # Use top 3 interests
            query = f"top tourist attractions in {destination} for {interest_str}"
        else:
            query = f"top tourist attractions in {destination}"
        
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=actual_limit))
        
        attractions = []
        for result in results:
            attractions.append({
                "name": result.get("title", "Unknown"),
                "description": result.get("body", "No description available")[:200],
                "source": result.get("href", "#")
            })
        
        if not attractions:
            return _get_fallback_attractions(destination, interests if isinstance(interests, list) else [])
        
        return attractions
    
    except Exception as e:
        print(f"Search error: {e}")
        return _get_fallback_attractions(destination, interests if isinstance(interests, list) else [])


def _get_fallback_attractions(destination: str, interests: List[str] = None) -> List[Dict[str, str]]:
    """Provide fallback attractions when search fails."""
    if interests is None:
        interests = []
    
    interest_topics = ", ".join(interests[:3]) if interests else "tourist attractions"
    
    return [
        {
            "name": f"Central {destination} City Tour",
            "description": f"Explore the main landmarks and cultural sites of {destination}. Focus on {interest_topics}.",
            "source": "#"
        },
        {
            "name": f"Local Markets of {destination}",
            "description": f"Experience authentic local culture and cuisine. Great for {interest_topics} enthusiasts.",
            "source": "#"
        },
        {
            "name": f"Historical {destination} Museum",
            "description": f"Learn about the rich history and heritage of {destination}.",
            "source": "#"
        },
        {
            "name": f"Food Tour in {destination}",
            "description": f"Sample local delicacies and street food across {destination}.",
            "source": "#"
        },
        {
            "name": f"Adventure Activities in {destination}",
            "description": f"Experience outdoor adventures and nature trails around {destination}.",
            "source": "#"
        }
    ]