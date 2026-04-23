"""
Virtual Scrolling Component for Large Tables
Implements efficient rendering of large datasets
"""

from typing import List, Dict, Any, Optional
import streamlit as st
import streamlit.components.v1 as components


def create_virtual_table(
    data: List[Dict[str, Any]],
    columns: List[str],
    row_height: int = 40,
    height: int = 400,
    key: str = "virtual_table"
) -> None:
    """
    Create a virtualized table for efficient rendering of large datasets.
    
    Args:
        data: List of row dictionaries
        columns: List of column names to display
        row_height: Height of each row in pixels
        height: Total table height in pixels
        key: Unique key for this component
    """
    if not data or not columns:
        st.info("No data to display")
        return
    
    # Calculate total rows
    total_rows = len(data)
    visible_rows = height // row_height
    buffer_rows = max(5, visible_rows // 2)
    
    # Create component HTML
    html = f"""
    <div id="{key}_container" style="height: {height}px; overflow-y: auto; position: relative;">
        <div id="{key}_viewport" style="position: relative;">
            <table style="width: 100%; border-collapse: collapse; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
                <thead>
                    <tr style="background: #F8F9FA; position: sticky; top: 0; z-index: 10;">
"""
    
    # Add column headers
    for col in columns:
        html += f"""
                        <th style="padding: 12px 16px; text-align: left; font-weight: 600; color: #1E3A5F; border-bottom: 2px solid #E5E7EB;">{col}</th>
"""
    
    html += """
                    </tr>
                </thead>
                <tbody id="{key}_body">
"""
    
    # Add placeholder rows (will be filled by JavaScript)
    for i in range(min(visible_rows + buffer_rows * 2, total_rows)):
        html += """
                    <tr style="height: """ + str(row_height) + """px;">
"""
        for col in columns:
            html += f"""
                        <td style="padding: 12px 16px; border-bottom: 1px solid #E5E7EB; vertical-align: middle;">{{{{data[{i}].{col} || ''}}}}</td>
"""
        html += """
                    </tr>
"""
    
    html += """
                </tbody>
            </table>
        </div>
    </div>
    
    <script>
    (function() {{
        const container = document.getElementById('{key}_container');
        const body = document.getElementById('{key}_body');
        const totalRows = {total_rows};
        const rowHeight = {row_height};
        const columns = {json_columns};
        const data = {json_data};
        const bufferRows = {buffer_rows};
        
        // Calculate visible range
        function getVisibleRange() {{
            const scrollTop = container.scrollTop;
            const visibleRowsCount = Math.ceil(container.clientHeight / rowHeight);
            const startRow = Math.max(0, Math.floor(scrollTop / rowHeight) - bufferRows);
            const endRow = Math.min(totalRows, startRow + visibleRowsCount + bufferRows * 2);
            return {{ start: startRow, end: endRow }};
        }}
        
        // Render visible rows
        function renderRows() {{
            const range = getVisibleRange();
            let html = '';
            
            for (let i = range.start; i < range.end; i++) {{
                html += '<tr style="height: ' + rowHeight + 'px;">';
                columns.forEach(function(col) {{
                    const value = data[i] && data[i][col] !== undefined ? data[i][col] : '';
                    html += '<td style="padding: 12px 16px; border-bottom: 1px solid #E5E7EB; vertical-align: middle;">' + value + '</td>';
                }});
                html += '</tr>';
            }}
            
            body.innerHTML = html;
            
            // Set container height
            container.style.height = (totalRows * rowHeight) + 'px';
        }}
        
        // Handle scroll
        container.addEventListener('scroll', function() {{
            renderRows();
        }});
        
        // Initial render
        renderRows();
    }})();
    </script>
    """
    
    components.html(html, height=height + 50, scrolling=False)


def create_virtual_list(
    items: List[str],
    item_height: int = 50,
    height: int = 400,
    key: str = "virtual_list"
) -> None:
    """
    Create a virtualized list for efficient rendering of long lists.
    
    Args:
        items: List of item strings
        item_height: Height of each item in pixels
        height: Total list height in pixels
        key: Unique key for this component
    """
    if not items:
        st.info("No items to display")
        return
    
    total_items = len(items)
    visible_items = height // item_height
    buffer_items = max(5, visible_items // 2)
    
    html = f"""
    <div id="{key}_container" style="height: {height}px; overflow-y: auto; position: relative;">
        <div id="{key}_viewport" style="position: relative;">
            <ul style="list-style: none; padding: 0; margin: 0;">
"""
    
    # Add placeholder items
    for i in range(min(visible_items + buffer_items * 2, total_items)):
        html += f"""
                <li style="height: {item_height}px; padding: 16px; border-bottom: 1px solid #E5E7EB; display: flex; align-items: center;">
                    <span style="color: #1E3A5F; font-weight: 500;">{{{{items[{i}]}}}}</span>
                </li>
"""
    
    html += """
            </ul>
        </div>
    </div>
    
    <script>
    (function() {{
        const container = document.getElementById('{key}_container');
        const viewport = document.getElementById('{key}_viewport');
        const totalItems = {total_items};
        const itemHeight = {item_height};
        const items = {json_items};
        const bufferItems = {buffer_items};
        
        function getVisibleRange() {{
            const scrollTop = container.scrollTop;
            const visibleItemsCount = Math.ceil(container.clientHeight / itemHeight);
            const startItem = Math.max(0, Math.floor(scrollTop / itemHeight) - bufferItems);
            const endItem = Math.min(totalItems, startItem + visibleItemsCount + bufferItems * 2);
            return {{ start: startItem, end: endItem }};
        }}
        
        function renderItems() {{
            const range = getVisibleRange();
            let html = '';
            
            for (let i = range.start; i < range.end; i++) {{
                html += '<li style="height: ' + itemHeight + 'px; padding: 16px; border-bottom: 1px solid #E5E7EB; display: flex; align-items: center;">';
                html += '<span style="color: #1E3A5F; font-weight: 500;">' + items[i] + '</span>';
                html += '</li>';
            }}
            
            viewport.querySelector('ul').innerHTML = html;
            container.style.height = (totalItems * itemHeight) + 'px';
        }}
        
        container.addEventListener('scroll', function() {{
            renderItems();
        }});
        
        renderItems();
    }})();
    </script>
    """
    
    components.html(html, height=height + 50, scrolling=False)


def create_data_table_with_virtual_scroll(
    data: List[Dict[str, Any]],
    columns: List[str],
    max_visible_rows: int = 100,
    key: str = "data_table"
) -> None:
    """
    Create a data table that uses virtual scrolling for large datasets.
    
    Args:
        data: List of row dictionaries
        columns: List of column names to display
        max_visible_rows: Maximum rows to show before virtual scrolling kicks in
        key: Unique key for this component
    """
    if not data or not columns:
        st.info("No data to display")
        return
    
    # Use regular table for small datasets
    if len(data) <= max_visible_rows:
        st.dataframe(data, width='stretch', hide_index=True)
        return
    
    # Use virtual scrolling for large datasets
    st.info(f"Displaying {len(data)} rows with virtual scrolling for performance")
    create_virtual_table(data, columns, key=key)
