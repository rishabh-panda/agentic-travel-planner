"""
Export Button State Management
Implements export button state management with tooltips
"""

from typing import Dict, Any, Optional
import streamlit as st
from components.export import export_to_txt, export_to_markdown, export_to_pdf
from components.export import create_export_filename, is_pdf_available
from components.sharing import copy_to_clipboard, create_email_share_link
from components.sharing import generate_shareable_link, show_share_options
from components.analytics import track_export_event, track_share_event
from components.feedback import show_feedback_confirmation


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
    col1, col2, col3 = st.columns(3)
    
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
            track_export_event(destination, "txt", True)
    
    with col2:
        # PDF Export
        if is_pdf_available():
            pdf_content = export_to_pdf(
                itinerary, destination, days, budget, currency,
                budget_info, weather_info
            )
            pdf_filename = create_export_filename(destination, "pdf")
            
            # Convert bytes to base64 for download
            import base64
            b64_pdf = base64.b64encode(pdf_content).decode()
            
            # Create download link with professional styling
            href = f'''
            <a href="data:application/pdf;base64,{b64_pdf}" download="{pdf_filename}" 
               style="display: inline-block; width: 100%; padding: 0.6rem 1.2rem; 
                      background: linear-gradient(135deg, #1E3A5F 0%, #008080 100%); 
                      color: white; text-decoration: none; border-radius: 8px; 
                      font-weight: 500; text-align: center; transition: all 0.2s ease;
                      box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                📄 Download PDF
            </a>
            '''
            st.markdown(href, unsafe_allow_html=True)
            track_export_event(destination, "pdf", True)
        else:
            st.markdown("""
            <div style="background-color: #FEF3C7; border-left: 4px solid #F59E0B; 
                        padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <strong>PDF Export Not Available</strong><br>
                PDF export requires the ReportLab library for professional document formatting.
                <br><br>
                <small>Install with: <code>pip install reportlab</code></small>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
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
            track_export_event(destination, "md", True)
    
    # Add sharing options
    st.markdown("")
    show_share_options(itinerary, destination, days, budget, currency)


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
        "pdf_enabled": enabled and is_pdf_available(),
        "md_enabled": enabled,
        "share_enabled": enabled
    }
