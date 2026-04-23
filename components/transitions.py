"""
Transition System Component for Agentic Travel Planner
Implements smooth transitions between progress and results
"""

from typing import Dict, Any, Optional
from datetime import datetime


class TransitionManager:
    """Manages UI transitions for smooth user experience"""
    
    def __init__(self):
        self.transition_states = {
            "idle": "idle",
            "generating": "generating",
            "transitioning": "transitioning",
            "results": "results"
        }
        self.current_state = "idle"
        self.transition_duration = 300  # milliseconds
        self.fade_duration = 500  # milliseconds
    
    def start_transition(self) -> Dict[str, Any]:
        """Start transition from progress to results"""
        self.current_state = "transitioning"
        
        return {
            "state": self.current_state,
            "transition_duration": self.transition_duration,
            "fade_duration": self.fade_duration,
            "animation": "fade-in"
        }
    
    def complete_transition(self) -> Dict[str, Any]:
        """Complete transition and show results"""
        self.current_state = "results"
        
        return {
            "state": self.current_state,
            "transition_duration": self.transition_duration,
            "fade_duration": self.fade_duration,
            "animation": "fade-in",
            "smooth": True
        }
    
    def reset(self) -> Dict[str, Any]:
        """Reset to idle state"""
        self.current_state = "idle"
        
        return {
            "state": self.current_state,
            "transition_duration": self.transition_duration,
            "fade_duration": self.fade_duration
        }
    
    def get_transition_css(self) -> Dict[str, str]:
        """Get CSS for smooth transitions"""
        return {
            "transition": f"opacity {self.fade_duration}ms ease, transform {self.fade_duration}ms ease",
            "opacity": "0",
            "transform": "translateY(10px)",
            "transition_timing_function": "ease",
            "transition_duration": f"{self.fade_duration}ms"
        }
    
    def get_results_css(self) -> Dict[str, str]:
        """Get CSS for results display"""
        return {
            "opacity": "1",
            "transform": "translateY(0)",
            "transition": f"opacity {self.fade_duration}ms ease, transform {self.fade_duration}ms ease"
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "current_state": self.current_state,
            "transition_states": self.transition_states,
            "transition_duration": self.transition_duration,
            "fade_duration": self.fade_duration
        }


# Initialize transition manager
transition_manager = TransitionManager()
