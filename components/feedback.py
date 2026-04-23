"""
Feedback Component for Post-Generation Feedback Prompt
Implements feedback collection and display
"""

from typing import Dict, Any, Optional
from datetime import datetime
import streamlit as st
from components.analytics import (
    should_show_feedback_prompt,
    record_feedback_prompt_shown,
    record_feedback_submitted,
    get_feedback_summary
)


def create_feedback_prompt(destination: str) -> bool:
    """
    Create a feedback prompt for users who return within 7 days.
    
    Args:
        destination: Travel destination
    
    Returns:
        True if feedback was submitted, False otherwise
    """
    if not should_show_feedback_prompt():
        return False
    
    # Record that prompt was shown
    record_feedback_prompt_shown(destination)
    
    # Display feedback prompt
    st.markdown("### How was your experience?")
    st.markdown("Please rate your travel plan generation experience:")
    
    # Rating stars
    rating = st.feedback("stars", key=f"feedback_rating_{destination}")
    
    if rating is not None:
        # Get optional comment
        comment = st.text_area(
            "Additional comments (optional):",
            key=f"feedback_comment_{destination}"
        )
        
        if st.button("Submit Feedback", key=f"feedback_submit_{destination}"):
            record_feedback_submitted(destination, rating + 1)
            st.success("Thank you for your feedback! We appreciate your input.")
            return True
    
    return False


def display_feedback_summary() -> None:
    """
    Display a summary of collected feedback.
    """
    summary = get_feedback_summary()
    
    if summary["total_feedback"] == 0:
        return
    
    st.markdown("### Feedback Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">⭐ {summary['average_rating']}/5</div>
            <div class="metric-label">Average Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{summary['total_feedback']}</div>
            <div class="metric-label">Total Feedbacks</div>
        </div>
        """, unsafe_allow_html=True)
    
    if summary["by_destination"]:
        st.markdown("#### By Destination")
        for dest, data in summary["by_destination"].items():
            st.markdown(f"- **{dest}**: ⭐ {data['average']}/5 ({data['count']} feedbacks)")


def create_feedback_form(
    destination: str,
    initial_rating: int = 3,
    initial_comment: str = ""
) -> Optional[Dict[str, Any]]:
    """
    Create a feedback form.
    
    Args:
        destination: Travel destination
        initial_rating: Initial rating value (1-5)
        initial_comment: Initial comment text
    
    Returns:
        Feedback data dictionary or None if not submitted
    """
    st.markdown("### Share Your Feedback")
    
    rating = st.slider(
        "Rating (1-5)",
        min_value=1,
        max_value=5,
        value=initial_rating,
        key=f"feedback_form_rating_{destination}"
    )
    
    comment = st.text_area(
        "Comments:",
        value=initial_comment,
        key=f"feedback_form_comment_{destination}"
    )
    
    if st.button("Submit Feedback", key=f"feedback_form_submit_{destination}"):
        record_feedback_submitted(destination, rating)
        return {
            "destination": destination,
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.now().isoformat()
        }
    
    return None


def show_feedback_confirmation(rating: int) -> None:
    """
    Show feedback submission confirmation.
    
    Args:
        rating: User rating (1-5)
    """
    st.markdown("### Thank You for Your Feedback! 🙏")
    
    st.markdown(f"""
    <div class="info-box">
        <strong>Your feedback (⭐ {rating}/5) has been recorded.</strong><br><br>
        We appreciate your input and will use it to improve our travel planning service.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### How We Use Your Feedback")
    st.markdown("""
    - **Improve AI-generated itineraries** - We analyze ratings to enhance our algorithms
    - **Enhance user experience** - Feedback helps us refine the interface
    - **Better destination recommendations** - Your preferences guide our suggestions
    - **Quality assurance** - Low ratings trigger quality review processes
    """)
    
    st.markdown("### What's Next?")
    st.markdown("""
    - You can generate new travel plans anytime
    - Your feedback helps us serve you better
    - Check back for improved recommendations
    """)
