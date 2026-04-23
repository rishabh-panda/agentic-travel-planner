"""
API Key Error Banner Component for Agentic Travel Planner
Implements prominent banner for missing or invalid API keys with clear instructions
"""

from typing import Dict, Any, Optional
import os


class APIKeyErrorBanner:
    """Manages API key error display and user guidance"""
    
    def __init__(self):
        self.error_types = {
            "missing": "missing",
            "invalid": "invalid",
            "placeholder": "placeholder"
        }
        self.env_file_path = ".env"
    
    def check_api_key_status(self) -> Dict[str, Any]:
        """
        Check API key status and return error information if needed.
        
        Returns:
            Dictionary with error status and guidance
        """
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            return {
                "has_error": True,
                "error_type": self.error_types["missing"],
                "message": "GROQ_API_KEY is not set",
                "severity": "critical",
                "instructions": [
                    "1. Create a .env file in the project root directory",
                    "2. Add your GROQ API key: GROQ_API_KEY=your_actual_key_here",
                    "3. Restart the application after updating .env"
                ],
                "link_to_docs": "https://console.groq.com/docs/quickstart",
                "env_file_path": self.env_file_path
            }
        
        if api_key == "your_groq_api_key_here":
            return {
                "has_error": True,
                "error_type": self.error_types["placeholder"],
                "message": "GROQ_API_KEY is using default placeholder",
                "severity": "warning",
                "instructions": [
                    "1. Open your .env file in the project root",
                    "2. Replace 'your_groq_api_key_here' with your actual GROQ API key",
                    "3. Save the file and restart the application"
                ],
                "link_to_docs": "https://console.groq.com/docs/quickstart",
                "env_file_path": self.env_file_path
            }
        
        return {
            "has_error": False,
            "error_type": None,
            "message": None,
            "severity": None,
            "instructions": None,
            "link_to_docs": None
        }
    
    def get_error_html(self, error_info: Dict[str, Any]) -> str:
        """
        Generate HTML for API key error banner.
        
        Args:
            error_info: Error information from check_api_key_status
        
        Returns:
            HTML string for error banner
        """
        if not error_info.get("has_error"):
            return ""
        
        error_type = error_info.get("error_type", "unknown")
        severity = error_info.get("severity", "critical")
        
        # Determine styling based on severity
        if severity == "critical":
            bg_color = "#FEE2E2"
            border_color = "#DC2626"
            icon = "❌"
        else:
            bg_color = "#FEF3C7"
            border_color = "#F59E0B"
            icon = "⚠️"
        
        instructions_html = ""
        if error_info.get("instructions"):
            instructions_html = "<ul style='margin: 0.5rem 0; padding-left: 1.5rem;'>"
            for instruction in error_info["instructions"]:
                instructions_html += f"<li style='margin: 0.25rem 0;'>{instruction}</li>"
            instructions_html += "</ul>"
        
        docs_link = ""
        if error_info.get("link_to_docs"):
            docs_link = f"<br><a href='{error_info['link_to_docs']}' target='_blank' style='color: #1E3A5F; text-decoration: underline;'>View API Key Setup Documentation</a>"
        
        return f"""
        <div class="api-key-banner" style="
            background-color: {bg_color};
            border-left: 4px solid {border_color};
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <strong style="color: #1E3A5F;">API Key Error:</strong>
                <span style="color: #1F2937;">{error_info.get('message', 'Unknown error')}</span>
            </div>
            {instructions_html}
            {docs_link}
            <br>
            <small style="color: #6B7280;">File location: <code>{error_info.get('env_file_path', '.env')}</code></small>
        </div>
        """
    
    def get_error_css(self) -> str:
        """
        Get CSS for API key error banner.
        
        Returns:
            CSS string for banner styling
        """
        return """
        .api-key-banner {
            animation: fadeIn 0.3s ease;
        }
        
        .api-key-banner a:hover {
            text-decoration: none;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        """
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "error_types": self.error_types,
            "env_file_path": self.env_file_path
        }
