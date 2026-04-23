"""
Generation Failure Error Box Component for Agentic Travel Planner
Implements dismissible error box with retry option for failed generations
"""

from typing import Dict, Any, Optional
import traceback


class GenerationErrorBox:
    """Manages generation failure error display and retry functionality"""
    
    def __init__(self):
        self.error_types = {
            "api_error": "api_error",
            "network_error": "network_error",
            "timeout_error": "timeout_error",
            "unknown_error": "unknown_error"
        }
        self.max_retry_attempts = 3
    
    def create_error_box(
        self,
        error_message: str,
        error_type: str = "unknown_error",
        error_details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create error box information for failed generation.
        
        Args:
            error_message: Main error message to display
            error_type: Type of error (api_error, network_error, etc.)
            error_details: Optional detailed error information
        
        Returns:
            Dictionary with error box configuration
        """
        # Determine error category and guidance
        error_category = self._categorize_error(error_type, error_message)
        
        return {
            "has_error": True,
            "error_message": error_message,
            "error_type": error_type,
            "error_category": error_category["category"],
            "severity": error_category["severity"],
            "instructions": error_category["instructions"],
            "retry_enabled": error_category["retry_enabled"],
            "error_details": error_details,
            "timestamp": error_details.get("timestamp") if error_details else None
        }
    
    def _categorize_error(
        self,
        error_type: str,
        error_message: str
    ) -> Dict[str, Any]:
        """
        Categorize error and determine appropriate response.
        
        Args:
            error_type: Type of error
            error_message: Error message text
        
        Returns:
            Dictionary with error category and guidance
        """
        error_lower = error_message.lower() if error_message else ""
        
        # API errors
        if "api" in error_lower or "groq" in error_lower:
            return {
                "category": self.error_types["api_error"],
                "severity": "high",
                "instructions": [
                    "Verify your API key is correct in the .env file",
                    "Check your internet connection",
                    "Try again in a few moments"
                ],
                "retry_enabled": True
            }
        
        # Network errors
        if "network" in error_lower or "connection" in error_lower or "timeout" in error_lower:
            return {
                "category": self.error_types["network_error"],
                "severity": "medium",
                "instructions": [
                    "Check your internet connection",
                    "Try again in a few moments",
                    "If the problem persists, try a different destination"
                ],
                "retry_enabled": True
            }
        
        # Timeout errors
        if "timeout" in error_lower or "timed out" in error_lower:
            return {
                "category": self.error_types["timeout_error"],
                "severity": "medium",
                "instructions": [
                    "The request took too long to complete",
                    "Try a simpler destination query",
                    "Reduce the number of days or budget complexity"
                ],
                "retry_enabled": True
            }
        
        # Unknown errors
        return {
            "category": self.error_types["unknown_error"],
            "severity": "high",
            "instructions": [
                "Please check your inputs and try again",
                "Verify your API key is configured correctly",
                "If the problem persists, contact support"
            ],
            "retry_enabled": True
        }
    
    def get_error_html(self, error_info: Dict[str, Any]) -> str:
        """
        Generate HTML for dismissible error box.
        
        Args:
            error_info: Error information from create_error_box
        
        Returns:
            HTML string for error box
        """
        if not error_info.get("has_error"):
            return ""
        
        severity = error_info.get("severity", "high")
        error_category = error_info.get("error_category", "unknown")
        
        # Determine styling based on severity
        if severity == "high":
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
        
        details_html = ""
        if error_info.get("error_details"):
            details_html = f"""
            <details style="margin-top: 0.5rem;">
                <summary style="cursor: pointer; color: #6B7280;">Show details</summary>
                <pre style="background: #F3F4F6; padding: 0.5rem; border-radius: 4px; margin: 0.5rem 0; font-size: 0.85rem;">{str(error_info['error_details'])}</pre>
            </details>
            """
        
        return f"""
        <div class="generation-error-box" style="
            background-color: {bg_color};
            border-left: 4px solid {border_color};
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <div style="flex: 1;">
                    <strong style="color: #1E3A5F;">Generation Failed:</strong>
                    <p style="margin: 0.5rem 0 0.5rem 0; color: #1F2937;">{error_info.get('error_message', 'Unknown error')}</p>
                    {instructions_html}
                    {details_html}
                    <div style="margin-top: 0.5rem;">
                        <button class="retry-btn" style="
                            background: linear-gradient(135deg, #1E3A5F 0%, #008080 100%);
                            color: white;
                            border: none;
                            border-radius: 6px;
                            padding: 0.5rem 1rem;
                            font-weight: 500;
                            cursor: pointer;
                            transition: all 0.2s ease;
                        ">Retry Generation</button>
                        <button class="close-btn" style="
                            background: transparent;
                            border: 1px solid #D1D5DB;
                            border-radius: 6px;
                            padding: 0.5rem 1rem;
                            font-weight: 500;
                            cursor: pointer;
                            margin-left: 0.5rem;
                            transition: all 0.2s ease;
                        ">Dismiss</button>
                    </div>
                </div>
            </div>
        </div>
        """
    
    def get_error_css(self) -> str:
        """
        Get CSS for generation error box.
        
        Returns:
            CSS string for error box styling
        """
        return """
        .generation-error-box {
            animation: fadeIn 0.3s ease;
        }
        
        .generation-error-box button:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .generation-error-box button:active {
            transform: translateY(0);
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
    
    def should_retry(self, error_info: Dict[str, Any]) -> bool:
        """
        Determine if error is retryable.
        
        Args:
            error_info: Error information from create_error_box
        
        Returns:
            True if error should be retried
        """
        if not error_info.get("has_error"):
            return False
        
        return error_info.get("retry_enabled", False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "error_types": self.error_types,
            "max_retry_attempts": self.max_retry_attempts
        }
