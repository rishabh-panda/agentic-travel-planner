"""
Export Button State Management
Implements export button state management with tooltips
"""

from typing import Dict, Any, Optional
import streamlit as st
from components.export import export_to_txt, export_to_markdown
from components.export import create_export_filename


def create_export_section(
    itinerary: str,
    destination: str,
    days: int,
    budget: float,
    currency: str,
    budget_info: Optional[Dict[str, Any]] = None,
    weather_info: Optional[Dict[str, Any]] = None
) -> None:
    """
    Create the export section with all export buttons.
    
    Args:
        itinerary: The itinerary content
        destination: Travel destination
        days: Number of days
        budget: Total budget
        currency: Currency code
        budget_info: Optional budget breakdown information
        weather_info: Optional weather information
    """
    st.markdown("### Export Options")
    
    # Check if results are available
    if not itinerary or not destination:
        st.info("Generate a travel plan to enable export functionality")
        return
    
    # Create export buttons
    col1, col2 = st.columns(2)
    
    with col1:
        # TXT Export
        txt_content = export_to_txt(itinerary, destination, days, budget, currency)
        txt_filename = create_export_filename(destination, "txt")
        
        if st.download_button(
            label="📄 Download TXT",
            data=txt_content,
            file_name=txt_filename,
            mime="text/plain",
            use_container_width=True,
            key="export_txt"
        ):
            pass
    
    with col2:
        # Markdown Export
        md_content = export_to_markdown(itinerary, destination, days, budget, currency)
        md_filename = create_export_filename(destination, "md")
        
        if st.download_button(
            label="📄 Download Markdown",
            data=md_content,
            file_name=md_filename,
            mime="text/markdown",
            use_container_width=True,
            key="export_md"
        ):
            pass


def is_export_enabled(itinerary: str, destination: str) -> bool:
    """
    Check if export functionality should be enabled.
    
    Args:
        itinerary: The itinerary content
        destination: Travel destination
    
    Returns:
        True if export is enabled
    """
    return bool(itinerary and destination)


def get_export_tooltip(itinerary: str, destination: str) -> str:
    """
    Get tooltip text for export buttons.
    
    Args:
        itinerary: The itinerary content
        destination: Travel destination
    
    Returns:
        Tooltip text
    """
    if not destination:
        return "Enter a destination to enable export"
    if not itinerary:
        return "Generate a travel plan to enable export"
    return ""


def create_export_button_group(
    itinerary: str,
    destination: str,
    days: int,
    budget: float,
    currency: str,
    budget_info: Optional[Dict[str, Any]] = None,
    weather_info: Optional[Dict[str, Any]] = None
) -> None:
    """
    Create a complete export button group with state management.
    
    Args:
        itinerary: The itinerary content
        destination: Travel destination
        days: Number of days
        budget: Total budget
        currency: Currency code
        budget_info: Optional budget breakdown information
        weather_info: Optional weather information
    """
    # Check if export is enabled
    if not is_export_enabled(itinerary, destination):
        st.markdown("### Export Options")
        st.info(get_export_tooltip(itinerary, destination))
        return
    
    # Create export section
    create_export_section(
        itinerary, destination, days, budget, currency,
        budget_info, weather_info
    )


def update_export_button_states(
    itinerary: str,
    destination: str
) -> Dict[str, bool]:
    """
    Update export button states based on current state.
    
    Args:
        itinerary: The itinerary content
        destination: Travel destination
    
    Returns:
        Dictionary of button states
    """
    enabled = is_export_enabled(itinerary, destination)
    
    return {
        "txt_enabled": enabled,
        "md_enabled": enabled
    }
