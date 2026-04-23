"""
Analytics Component for Event Tracking
Implements anonymized event tracking, feedback prompts, and heat map data collection
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import hashlib
import json
import streamlit as st


# Session ID for anonymized user tracking
def get_anonymized_session_id() -> str:
    """
    Generate a hashed session ID for anonymized user tracking.
    
    Returns:
        Hashed session ID string
    """
    if "session_id" not in st.session_state:
        # Generate a unique session ID
        import uuid
        session_id = str(uuid.uuid4())
        st.session_state.session_id = session_id
    
    # Hash the session ID for anonymity
    return hashlib.sha256(st.session_state.session_id.encode()).hexdigest()[:16]


def get_session_start_time() -> datetime:
    """
    Get the session start time.
    
    Returns:
        Session start datetime
    """
    if "session_start" not in st.session_state:
        st.session_state.session_start = datetime.now()
    return st.session_state.session_start


def calculate_budget_range(budget: float, currency: str = "INR") -> str:
    """
    Calculate budget range category.
    
    Args:
        budget: Total budget amount
        currency: Currency code
    
    Returns:
        Budget range category ("low", "medium", "high")
    """
    # Convert to USD equivalent for comparison (approximate)
    conversion_rates = {
        "INR": 0.012,
        "USD": 1.0,
        "EUR": 1.08,
        "GBP": 1.27,
        "JPY": 0.0067,
        "CAD": 0.74,
        "AUD": 0.66,
        "SGD": 0.75,
        "CNY": 0.14
    }
    
    rate = conversion_rates.get(currency, 0.012)
    budget_usd = budget * rate
    
    if budget_usd < 500:
        return "low"
    elif budget_usd < 2000:
        return "medium"
    else:
        return "high"


def calculate_destination_type(destination: str) -> str:
    """
    Determine destination type based on destination name.
    
    Args:
        destination: Destination name
    
    Returns:
        Destination type ("domestic" or "international")
    """
    # Simple heuristic - in a real app, this would use a database of countries
    destination_lower = destination.lower()
    
    # Common domestic destinations (for India example)
    domestic_keywords = ["delhi", "mumbai", "bangalore", "chennai", "kolkata", 
                        "goa", "kerala", "rajasthan", "uttarakhand", "himachal"]
    
    # Check if destination matches domestic keywords
    for keyword in domestic_keywords:
        if keyword in destination_lower:
            return "domestic"
    
    return "international"


def track_generation_event(
    destination: str,
    days: int,
    budget: float,
    currency: str,
    generation_time: float,
    success: bool = True
) -> Dict[str, Any]:
    """
    Track a generation event with anonymized metrics.
    
    Args:
        destination: Travel destination
        days: Number of days
        budget: Total budget
        currency: Currency code
        generation_time: Time taken for generation in seconds
        success: Whether generation was successful
    
    Returns:
        Event data dictionary
    """
    event_data = {
        "event_type": "generation_complete",
        "destination": destination,
        "destination_type": calculate_destination_type(destination),
        "budget_range": calculate_budget_range(budget, currency),
        "days": days,
        "generation_time_seconds": round(generation_time, 2),
        "success": success,
        "timestamp": datetime.now().isoformat(),
        "anonymized_user_id": get_anonymized_session_id(),
        "session_start": get_session_start_time().isoformat()
    }
    
    # Store in session state for later retrieval
    if "analytics_events" not in st.session_state:
        st.session_state.analytics_events = []
    
    st.session_state.analytics_events.append(event_data)
    
    return event_data


def track_export_event(
    destination: str,
    format_type: str,
    success: bool = True
) -> Dict[str, Any]:
    """
    Track an export event.
    
    Args:
        destination: Travel destination
        format_type: Export format (txt, pdf, md)
        success: Whether export was successful
    
    Returns:
        Event data dictionary
    """
    event_data = {
        "event_type": "export",
        "destination": destination,
        "format_type": format_type,
        "success": success,
        "timestamp": datetime.now().isoformat(),
        "anonymized_user_id": get_anonymized_session_id()
    }
    
    if "analytics_events" not in st.session_state:
        st.session_state.analytics_events = []
    
    st.session_state.analytics_events.append(event_data)
    
    return event_data


def track_share_event(
    destination: str,
    share_type: str,
    success: bool = True
) -> Dict[str, Any]:
    """
    Track a share event.
    
    Args:
        destination: Travel destination
        share_type: Share type (copy, email, link)
        success: Whether share was successful
    
    Returns:
        Event data dictionary
    """
    event_data = {
        "event_type": "share",
        "destination": destination,
        "share_type": share_type,
        "success": success,
        "timestamp": datetime.now().isoformat(),
        "anonymized_user_id": get_anonymized_session_id()
    }
    
    if "analytics_events" not in st.session_state:
        st.session_state.analytics_events = []
    
    st.session_state.analytics_events.append(event_data)
    
    return event_data


def track_heat_map_event(
    element_id: str,
    interaction_type: str,
    position: Optional[Dict[str, int]] = None
) -> Dict[str, Any]:
    """
    Track a heat map event for popular sections/elements.
    
    Args:
        element_id: ID of the interacted element
        interaction_type: Type of interaction (click, hover, scroll)
        position: Optional position data (x, y coordinates)
    
    Returns:
        Event data dictionary
    """
    event_data = {
        "event_type": "heat_map",
        "element_id": element_id,
        "interaction_type": interaction_type,
        "timestamp": datetime.now().isoformat(),
        "anonymized_user_id": get_anonymized_session_id()
    }
    
    if position:
        event_data["position"] = position
    
    if "analytics_events" not in st.session_state:
        st.session_state.analytics_events = []
    
    st.session_state.analytics_events.append(event_data)
    
    return event_data


def track_feedback_event(
    destination: str,
    rating: int,
    comment: str = "",
    timestamp: datetime = None
) -> Dict[str, Any]:
    """
    Track a feedback event.
    
    Args:
        destination: Travel destination
        rating: User rating (1-5)
        comment: Optional feedback comment
        timestamp: Optional timestamp
    
    Returns:
        Event data dictionary
    """
    event_data = {
        "event_type": "feedback",
        "destination": destination,
        "rating": rating,
        "comment": comment,
        "timestamp": (timestamp or datetime.now()).isoformat(),
        "anonymized_user_id": get_anonymized_session_id()
    }
    
    if "analytics_events" not in st.session_state:
        st.session_state.analytics_events = []
    
    st.session_state.analytics_events.append(event_data)
    
    return event_data


def get_analytics_data() -> List[Dict[str, Any]]:
    """
    Get all collected analytics data.
    
    Returns:
        List of all analytics events
    """
    return st.session_state.get("analytics_events", [])


def clear_analytics_data() -> None:
    """
    Clear all collected analytics data.
    """
    if "analytics_events" in st.session_state:
        st.session_state.analytics_events = []


def should_show_feedback_prompt() -> bool:
    """
    Check if feedback prompt should be shown.
    
    Returns:
        True if user should be prompted for feedback
    """
    # Check if user has generated a plan before
    if "last_generation_time" not in st.session_state:
        return False
    
    # Check if 7 days have passed since last generation
    last_generation = st.session_state.last_generation_time
    days_since = (datetime.now() - last_generation).days
    
    if days_since < 7:
        return False
    
    # Check if feedback was already given for this destination
    if "feedback_given" not in st.session_state:
        return True
    
    return False


def record_feedback_prompt_shown(destination: str) -> None:
    """
    Record that feedback prompt was shown for a destination.
    
    Args:
        destination: Travel destination
    """
    if "feedback_prompts_shown" not in st.session_state:
        st.session_state.feedback_prompts_shown = []
    
    st.session_state.feedback_prompts_shown.append({
        "destination": destination,
        "timestamp": datetime.now().isoformat()
    })


def record_feedback_submitted(destination: str, rating: int) -> None:
    """
    Record that feedback was submitted for a destination.
    
    Args:
        destination: Travel destination
        rating: User rating (1-5)
    """
    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = []
    
    st.session_state.feedback_submitted.append({
        "destination": destination,
        "rating": rating,
        "timestamp": datetime.now().isoformat()
    })


def get_feedback_summary() -> Dict[str, Any]:
    """
    Get feedback summary statistics.
    
    Returns:
        Dictionary with feedback statistics
    """
    feedback = st.session_state.get("feedback_submitted", [])
    
    if not feedback:
        return {
            "total_feedback": 0,
            "average_rating": 0,
            "by_destination": {}
        }
    
    ratings = [f["rating"] for f in feedback]
    
    by_destination = {}
    for f in feedback:
        dest = f["destination"]
        if dest not in by_destination:
            by_destination[dest] = []
        by_destination[dest].append(f["rating"])
    
    return {
        "total_feedback": len(feedback),
        "average_rating": round(sum(ratings) / len(ratings), 2),
        "by_destination": {
            dest: {
                "count": len(ratings),
                "average": round(sum(ratings) / len(ratings), 2)
            }
            for dest, ratings in by_destination.items()
        }
    }


def export_analytics_data() -> str:
    """
    Export analytics data as JSON string.
    
    Returns:
        JSON string of analytics data
    """
    data = {
        "exported_at": datetime.now().isoformat(),
        "events": get_analytics_data(),
        "feedback_summary": get_feedback_summary()
    }
    return json.dumps(data, indent=2)
