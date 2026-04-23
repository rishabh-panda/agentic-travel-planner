"""
Input Validation Component for Agentic Travel Planner
Implements validation with appropriate feedback
"""

from typing import Dict, Any, Optional, Tuple
from datetime import datetime


class InputValidator:
    """Validates user input with appropriate feedback"""
    
    def __init__(self):
        self.validation_rules = {
            "destination": {"min_length": 3, "max_length": 100},
            "interests": {"min_length": 0, "max_length": 500},
            "days": {"min_value": 1, "max_value": 365},
            "budget": {"min_value": 0.01, "max_value": 1000000}
        }
        self.validation_errors = []
    
    def validate_destination(self, destination: str) -> Tuple[bool, Optional[str]]:
        """Validate destination input"""
        if not destination:
            return False, "Destination is required"
        
        min_length = self.validation_rules["destination"]["min_length"]
        max_length = self.validation_rules["destination"]["max_length"]
        
        if len(destination) < min_length:
            return False, f"Please enter at least {min_length} characters"
        
        if len(destination) > max_length:
            return False, f"Destination name is too long (max {max_length} characters)"
        
        return True, None
    
    def validate_interests(self, interests: str) -> Tuple[bool, Optional[str]]:
        """Validate interests input"""
        if not interests:
            return True, None  # Empty is valid
        
        min_length = self.validation_rules["interests"]["min_length"]
        max_length = self.validation_rules["interests"]["max_length"]
        
        if len(interests) < min_length:
            return False, f"Interests must be at least {min_length} characters"
        
        if len(interests) > max_length:
            return False, f"Interests are too long (max {max_length} characters)"
        
        return True, None
    
    def validate_days(self, days: int) -> Tuple[bool, Optional[str]]:
        """Validate days input"""
        if days is None:
            return False, "Number of days is required"
        
        min_value = self.validation_rules["days"]["min_value"]
        max_value = self.validation_rules["days"]["max_value"]
        
        if days < min_value:
            return False, f"Trip must be at least {min_value} day(s)"
        
        if days > max_value:
            return False, f"Trip cannot exceed {max_value} days"
        
        return True, None
    
    def validate_budget(self, budget: float) -> Tuple[bool, Optional[str]]:
        """Validate budget input"""
        if budget is None:
            return False, "Budget is required"
        
        min_value = self.validation_rules["budget"]["min_value"]
        max_value = self.validation_rules["budget"]["max_value"]
        
        if budget < min_value:
            return False, f"Budget must be greater than {min_value}"
        
        if budget > max_value:
            return False, f"Budget cannot exceed {max_value:,.0f}"
        
        return True, None
    
    def validate_all(self, data: Dict[str, Any]) -> Tuple[bool, list]:
        """Validate all inputs"""
        errors = []
        
        # Validate destination
        valid, error = self.validate_destination(data.get("destination", ""))
        if not valid:
            errors.append({"field": "destination", "message": error})
        
        # Validate interests
        valid, error = self.validate_interests(data.get("interests", ""))
        if not valid:
            errors.append({"field": "interests", "message": error})
        
        # Validate days
        valid, error = self.validate_days(data.get("days"))
        if not valid:
            errors.append({"field": "days", "message": error})
        
        # Validate budget
        valid, error = self.validate_budget(data.get("budget"))
        if not valid:
            errors.append({"field": "budget", "message": error})
        
        return len(errors) == 0, errors
    
    def add_validation_error(self, field: str, message: str) -> None:
        """Add a validation error"""
        self.validation_errors.append({
            "field": field,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
    
    def clear_validation_errors(self) -> None:
        """Clear all validation errors"""
        self.validation_errors = []
    
    def get_validation_errors(self) -> list:
        """Get all validation errors"""
        return self.validation_errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "validation_rules": self.validation_rules,
            "validation_errors": self.validation_errors
        }


# Initialize validator
validator = InputValidator()
