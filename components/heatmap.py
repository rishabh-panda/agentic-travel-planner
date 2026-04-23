"""
Heat Map Component for User Interaction Tracking
Implements heat map data collection for popular sections and elements
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import streamlit as st
from components.analytics import track_heat_map_event


def track_element_interaction(
    element_id: str,
    interaction_type: str = "click",
    position: Optional[Dict[str, int]] = None
) -> None:
    """
    Track an element interaction for heat map data.
    
    Args:
        element_id: ID of the interacted element
        interaction_type: Type of interaction (click, hover, scroll)
        position: Optional position data (x, y coordinates)
    """
    track_heat_map_event(element_id, interaction_type, position)


def track_section_view(section_id: str, duration_seconds: float = 0.0) -> None:
    """
    Track when a user views a section.
    
    Args:
        section_id: ID of the viewed section
        duration_seconds: How long the user viewed the section
    """
    track_heat_map_event(section_id, "view", {"duration": duration_seconds})


def track_scroll_depth(depth_percentage: float) -> None:
    """
    Track scroll depth for heat map data.
    
    Args:
        depth_percentage: Percentage of page scrolled (0-100)
    """
    track_heat_map_event("scroll_depth", "scroll", {"depth": depth_percentage})


def get_heat_map_data() -> Dict[str, Any]:
    """
    Get collected heat map data.
    
    Returns:
        Dictionary with heat map statistics
    """
    events = st.session_state.get("analytics_events", [])
    
    # Filter heat map events
    heat_map_events = [e for e in events if e.get("event_type") == "heat_map"]
    
    # Aggregate by element_id
    element_stats = {}
    for event in heat_map_events:
        element_id = event.get("element_id", "unknown")
        interaction_type = event.get("interaction_type", "unknown")
        
        if element_id not in element_stats:
            element_stats[element_id] = {
                "total_interactions": 0,
                "interactions_by_type": {}
            }
        
        element_stats[element_id]["total_interactions"] += 1
        
        if interaction_type not in element_stats[element_id]["interactions_by_type"]:
            element_stats[element_id]["interactions_by_type"][interaction_type] = 0
        
        element_stats[element_id]["interactions_by_type"][interaction_type] += 1
    
    # Sort by most interacted
    sorted_elements = sorted(
        element_stats.items(),
        key=lambda x: x[1]["total_interactions"],
        reverse=True
    )
    
    return {
        "total_heat_map_events": len(heat_map_events),
        "unique_elements": len(element_stats),
        "element_stats": dict(sorted_elements[:10]),  # Top 10 elements
        "collected_at": datetime.now().isoformat()
    }


def get_popular_sections() -> List[Dict[str, Any]]:
    """
    Get list of most popular sections based on heat map data.
    
    Returns:
        List of popular sections with interaction counts
    """
    data = get_heat_map_data()
    
    popular = []
    for element_id, stats in data.get("element_stats", {}).items():
        popular.append({
            "element_id": element_id,
            "total_interactions": stats["total_interactions"],
            "interaction_types": stats["interactions_by_type"]
        })
    
    return popular


def display_heat_map_summary() -> None:
    """
    Display a summary of heat map data.
    """
    data = get_heat_map_data()
    
    if data["total_heat_map_events"] == 0:
        return
    
    st.markdown("### User Interaction Heat Map")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{data['total_heat_map_events']}</div>
            <div class="metric-label">Total Interactions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{data['unique_elements']}</div>
            <div class="metric-label">Unique Elements</div>
        </div>
        """, unsafe_allow_html=True)
    
    popular = get_popular_sections()
    if popular:
        st.markdown("#### Most Interacted Elements")
        for item in popular[:5]:
            st.markdown(f"- **{item['element_id']}**: {item['total_interactions']} interactions")


def create_heat_map_tracker() -> str:
    """
    Create JavaScript for client-side heat map tracking.
    
    Returns:
        JavaScript code string
    """
    return """
    <script>
    // Track element clicks
    document.addEventListener('click', function(e) {
        const element = e.target;
        const elementId = element.id || element.className || 'unknown';
        
        // Send interaction data to Streamlit
        if (window.parent && window.parent.postMessage) {
            window.parent.postMessage({
                type: 'heat_map_interaction',
                element_id: elementId,
                interaction_type: 'click',
                position: {
                    x: e.clientX,
                    y: e.clientY
                }
            }, '*');
        }
    });
    
    // Track scroll depth
    let lastScrollPosition = 0;
    document.addEventListener('scroll', function() {
        const scrollTop = window.scrollY;
        const docHeight = document.body.scrollHeight;
        const winHeight = window.innerHeight;
        const scrollPercent = (scrollTop / (docHeight - winHeight)) * 100;
        
        if (scrollPercent > lastScrollPosition) {
            lastScrollPosition = scrollPercent;
            
            // Send scroll data to Streamlit
            if (window.parent && window.parent.postMessage) {
                window.parent.postMessage({
                    type: 'heat_map_scroll',
                    depth: scrollPercent
                }, '*');
            }
        }
    });
    
    // Track hover events
    document.addEventListener('mouseover', function(e) {
        const element = e.target;
        const elementId = element.id || element.className || 'unknown';
        
        // Send hover data to Streamlit
        if (window.parent && window.parent.postMessage) {
            window.parent.postMessage({
                type: 'heat_map_interaction',
                element_id: elementId,
                interaction_type: 'hover'
            }, '*');
        }
    });
    </script>
    """


def get_element_heat_map(element_id: str) -> Dict[str, Any]:
    """
    Get heat map data for a specific element.
    
    Args:
        element_id: ID of the element
    
    Returns:
        Dictionary with element heat map data
    """
    data = get_heat_map_data()
    element_stats = data.get("element_stats", {})
    
    if element_id in element_stats:
        return {
            "element_id": element_id,
            "total_interactions": element_stats[element_id]["total_interactions"],
            "interaction_types": element_stats[element_id]["interactions_by_type"],
            "rank": list(element_stats.keys()).index(element_id) + 1
        }
    
    return {
        "element_id": element_id,
        "total_interactions": 0,
        "interaction_types": {},
        "rank": None
    }
