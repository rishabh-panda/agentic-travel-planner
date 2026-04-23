"""
Date Range Validation Component for Agentic Travel Planner
Implements date range validation to prevent invalid submissions
"""

from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta


class DateRangeValidator:
    """Validates date ranges for travel planning"""
    
    def __init__(self):
        self.max_days = 365
        self.min_days = 1
        self.max_budget = 1000000
        self.min_budget = 0.01
    
    def validate_days(self, days: int) -> Tuple[bool, Optional[str]]:
        """Validate number of days"""
        if days is None:
            return False, "Number of days is required"
        
        if not isinstance(days, (int, float)):
            return False, "Number of days must be a number"
        
        if days < self.min_days:
            return False, f"Trip must be at least {self.min_days} day(s)"
        
        if days > self.max_days:
            return False, f"Trip cannot exceed {self.max_days} days"
        
        return True, None
    
    def validate_budget(self, budget: float) -> Tuple[bool, Optional[str]]:
        """Validate budget"""
        if budget is None:
            return False, "Budget is required"
        
        if not isinstance(budget, (int, float)):
            return False, "Budget must be a number"
        
        if budget < self.min_budget:
            return False, f"Budget must be greater than {self.min_budget:,.2f}"
        
        if budget > self.max_budget:
            return False, f"Budget cannot exceed {self.max_budget:,.0f}"
        
        return True, None
    
    def validate_date_range(self, days: int, budget: float) -> Tuple[bool, list]:
        """Validate date range and budget together"""
        errors = []
        
        # Validate days
        valid, error = self.validate_days(days)
        if not valid:
            errors.append({"field": "days", "message": error})
        
        # Validate budget
        valid, error = self.validate_budget(budget)
        if not valid:
            errors.append({"field": "budget", "message": error})
        
        # Check budget per day ratio
        if days and budget and days > 0:
            daily_budget = budget / days
            if daily_budget < 1:
                errors.append({
                    "field": "budget",
                    "message": f"Daily budget ({daily_budget:.2f}) is too low. Consider increasing total budget."
                })
        
        return len(errors) == 0, errors
    
    def validate_trip_dates(self, start_date: str, end_date: str) -> Tuple[bool, Optional[str]]:
        """Validate trip date range"""
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            
            if start >= end:
                return False, "End date must be after start date"
            
            if start < datetime.now():
                return False, "Start date cannot be in the past"
            
            # Calculate days
            days = (end - start).days + 1
            if days > self.max_days:
                return False, f"Trip duration cannot exceed {self.max_days} days"
            
            return True, None
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"
    
    def get_valid_date_range(self, days: int) -> Dict[str, str]:
        """Get valid date range for specified days"""
        today = datetime.now().date()
        min_start = today
        max_start = today + timedelta(days=self.max_days - days)
        
        min_end = min_start + timedelta(days=days - 1)
        max_end = max_start + timedelta(days=days - 1)
        
        return {
            "min_start": min_start.isoformat(),
            "max_start": max_start.isoformat(),
            "min_end": min_end.isoformat(),
            "max_end": max_end.isoformat()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "max_days": self.max_days,
            "min_days": self.min_days,
            "max_budget": self.max_budget,
            "min_budget": self.min_budget
        }


# Initialize date range validator
date_range_validator = DateRangeValidator()
