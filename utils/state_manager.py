from typing import Dict, Any, Optional
from datetime import datetime
import json


class StateManager:
    """Manages the shared state across all agents."""
    
    def __init__(self):
        self.state = {
            "user_input": {},
            "research": {},
            "budget": {},
            "logistics": {},
            "final_itinerary": None,
            "errors": [],
            "checkpoints": {}
        }
    
    def get_state(self) -> Dict[str, Any]:
        """Return current state."""
        return self.state
    
    def update_state(self, key: str, value: Any) -> None:
        """Update a specific state key."""
        if key not in self.state:
            raise ValueError(f"Invalid state key: {key}")
        self.state[key] = value
    
    def update_nested_state(self, path: str, value: Any) -> None:
        """Update nested state using dot notation (e.g., 'research.attractions')."""
        keys = path.split('.')
        current = self.state
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
    
    def get_nested_state(self, path: str, default: Any = None) -> Any:
        """Get nested state value."""
        keys = path.split('.')
        current = self.state
        
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return default
            current = current[key]
        
        return current
    
    def add_error(self, error_message: str) -> None:
        """Log an error to state."""
        self.state["errors"].append({
            "timestamp": datetime.now().isoformat(),
            "message": error_message
        })
    
    def set_checkpoint(self, checkpoint_name: str, data: Any) -> None:
        """Save checkpoint data for human-in-the-loop."""
        self.state["checkpoints"][checkpoint_name] = data
    
    def get_checkpoint(self, checkpoint_name: str) -> Optional[Any]:
        """Retrieve checkpoint data."""
        return self.state["checkpoints"].get(checkpoint_name)
    
    def reset(self) -> None:
        """Reset state for new itinerary."""
        self.__init__()