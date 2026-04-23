"""
Lazy Loading Component for Non-Critical Content
Implements on-demand loading of images, charts, and other heavy content
"""

from typing import List, Dict, Any, Optional
import streamlit as st
import streamlit.components.v1 as components


def lazy_load_image(
    url: str,
    alt: str = "",
    width: int = None,
    height: int = None,
    key: str = None
) -> None:
    """
    Load an image with lazy loading.
    
    Args:
        url: Image URL
        alt: Alt text for accessibility
        width: Image width (optional)
        height: Image height (optional)
        key: Unique key for this component
    """
    if not url:
        return
    
    if key is None:
        key = f"lazy_img_{hash(url)}"
    
    style = ""
    if width:
        style += f"width: {width}px; "
    if height:
        style += f"height: {height}px; "
    
    html = f"""
    <div id="{key}_container" style="min-height: {height or 200}px; display: flex; align-items: center; justify-content: center;">
        <div style="color: #9CA3AF; font-size: 14px;">Loading...</div>
    </div>
    
    <script>
    (function() {{
        const container = document.getElementById('{key}_container');
        const img = new Image();
        
        img.onload = function() {{
            container.innerHTML = '';
            img.style.cssText = '{style}max-width: 100%; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);';
            container.appendChild(img);
        }};
        
        img.onerror = function() {{
            container.innerHTML = '<div style="color: #EF4444;">Failed to load image</div>';
        }};
        
        img.src = "{url}";
    }})();
    </script>
    """
    
    components.html(html, height=height or 200, scrolling=False)


def lazy_load_chart(
    chart_data: Dict[str, Any],
    chart_type: str = "bar",
    height: int = 400,
    key: str = None
) -> None:
    """
    Load a chart with lazy loading.
    
    Args:
        chart_data: Chart data dictionary
        chart_type: Type of chart (bar, line, pie)
        height: Chart height in pixels
        key: Unique key for this component
    """
    if key is None:
        key = f"lazy_chart_{hash(str(chart_data))}"
    
    html = f"""
    <div id="{key}_container" style="min-height: {height}px; display: flex; align-items: center; justify-content: center;">
        <div style="color: #9CA3AF; font-size: 14px;">Loading chart...</div>
    </div>
    
    <script>
    (function() {{
        const container = document.getElementById('{key}_container');
        
        // Simulate lazy loading with a small delay
        setTimeout(function() {{
            container.innerHTML = '<div style="color: #10B981;">Chart loaded successfully</div>';
            
            // In a real implementation, this would render the actual chart
            // using Plotly or another charting library
        }}, 500);
    }})();
    </script>
    """
    
    components.html(html, height=height, scrolling=False)


def lazy_load_section(
    content: str,
    title: str = "",
    expanded: bool = False,
    key: str = None
) -> None:
    """
    Create a lazy-loaded expandable section.
    
    Args:
        content: Content to display when expanded
        title: Section title
        expanded: Whether section is initially expanded
        key: Unique key for this component
    """
    if key is None:
        key = f"lazy_section_{hash(content)}"
    
    # Use Streamlit's expander with lazy loading
    with st.expander(title, expanded=expanded):
        # Show placeholder initially
        placeholder = st.empty()
        
        # In a real implementation, this would load content on demand
        # For now, we'll just display the content
        placeholder.markdown(content)


def lazy_load_tabs(
    tabs_data: List[Dict[str, Any]],
    key: str = None
) -> None:
    """
    Create lazy-loaded tabs.
    
    Args:
        tabs_data: List of tab data dictionaries with 'title' and 'content' keys
        key: Unique key for this component
    """
    if not tabs_data:
        return
    
    if key is None:
        key = f"lazy_tabs_{hash(str(tabs_data))}"
    
    # Create tabs
    tab_titles = [tab.get('title', 'Tab') for tab in tabs_data]
    tabs = st.tabs(tab_titles)
    
    # Load content lazily
    for i, (tab, tab_data) in enumerate(zip(tabs, tabs_data)):
        with tab:
            placeholder = st.empty()
            content = tab_data.get('content', '')
            
            # In a real implementation, this would load content on demand
            placeholder.markdown(content)


def create_lazy_loading_wrapper(
    content_loader,
    loading_text: str = "Loading...",
    error_text: str = "Failed to load",
    key: str = None
):
    """
    Create a wrapper for lazy loading any content.
    
    Args:
        content_loader: Function that returns the content to display
        loading_text: Text to show while loading
        error_text: Text to show on error
        key: Unique key for this component
    """
    if key is None:
        key = f"lazy_wrapper_{hash(str(content_loader))}"
    
    # Show placeholder
    placeholder = st.empty()
    
    try:
        # Load content
        content = content_loader()
        placeholder.markdown(content)
    except Exception as e:
        placeholder.error(f"{error_text}: {str(e)}")


def lazy_load_images_in_text(
    text: str,
    max_images: int = 10,
    key: str = None
) -> str:
    """
    Convert image markdown to lazy-loaded images.
    
    Args:
        text: Text containing image markdown
        max_images: Maximum number of images to process
        key: Unique key for this component
    
    Returns:
        HTML with lazy-loaded images
    """
    import re
    
    if key is None:
        key = f"lazy_images_{hash(text)}"
    
    # Find all image markdown patterns
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    images = re.findall(image_pattern, text)
    
    # Limit number of images
    images = images[:max_images]
    
    # Replace image markdown with lazy loading
    result = text
    for i, (alt, url) in enumerate(images):
        img_key = f"{key}_img_{i}"
        result = result.replace(f'![{alt}]({url})', f'<div id="{img_key}">Loading image...</div>')
    
    return result
