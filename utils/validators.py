from typing import Dict, Any, List
from decimal import Decimal, ROUND_HALF_UP


def validate_budget_input(request: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize budget request input."""
    
    validated = request.copy()
    
    # Validate total_budget
    if "total_budget" not in validated:
        raise ValueError("total_budget is required")
    if validated["total_budget"] <= 0:
        raise ValueError("total_budget must be greater than 0")
    if validated["total_budget"] > 1000000:
        raise ValueError("total_budget exceeds maximum allowed (1,000,000)")
    
    # Validate currency
    if "currency" not in validated:
        validated["currency"] = "USD"
    validated["currency"] = validated["currency"].upper()
    if len(validated["currency"]) != 3:
        raise ValueError("currency must be a 3-letter code")
    
    # Validate days
    if "days" not in validated:
        raise ValueError("days is required")
    if validated["days"] <= 0:
        raise ValueError("days must be greater than 0")
    if validated["days"] > 365:
        raise ValueError("days cannot exceed 365")
    
    # Validate destination
    if "destination" not in validated:
        raise ValueError("destination is required")
    if len(validated["destination"]) < 2:
        raise ValueError("destination must be at least 2 characters")
    
    # Set defaults for optional fields
    validated.setdefault("traveller_type", "mid-range")
    validated.setdefault("group_size", 1)
    validated.setdefault("booking_window_days", 60)
    validated.setdefault("include_hidden_costs", True)
    validated.setdefault("risk_tolerance", "medium")
    validated.setdefault("travel_style_priorities", [])
    
    # Validate traveller_type
    valid_types = ["budget", "mid-range", "luxury"]
    if validated["traveller_type"] not in valid_types:
        validated["traveller_type"] = "mid-range"
    
    # Validate group_size
    if validated["group_size"] < 1:
        validated["group_size"] = 1
    if validated["group_size"] > 50:
        validated["group_size"] = 50
    
    # Validate booking_window_days
    if validated["booking_window_days"] < 0:
        validated["booking_window_days"] = 0
    if validated["booking_window_days"] > 365:
        validated["booking_window_days"] = 365
    
    # Validate risk_tolerance
    valid_risks = ["low", "medium", "high"]
    if validated["risk_tolerance"] not in valid_risks:
        validated["risk_tolerance"] = "medium"
    
    return validated


def validate_currency(currency: str, supported_currencies: List[str]) -> bool:
    """Validate if currency is supported."""
    return currency.upper() in supported_currencies


def round_decimal(value: float, places: int = 2) -> float:
    """Round decimal to specified places using proper rounding."""
    decimal_value = Decimal(str(value))
    rounded = decimal_value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return float(rounded)