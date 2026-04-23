from typing import Dict, Any
import yaml
import os


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    default_config = {
        "llm_model": "llama-3.3-70b-versatile",
        "base_currency": "USD",
        "enable_hidden_cost_detection": True,
        "enable_price_prediction": True,
        "cache_duration_hours": 24
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                if config:
                    default_config.update(config)
        except Exception as e:
            print(f"Error loading config: {e}")
    
    return default_config


def format_currency(amount: float, currency: str) -> str:
    """Format amount with currency symbol."""
    symbols = {
        "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥",
        "INR": "₹", "CNY": "¥", "SGD": "S$", "CAD": "C$", "AUD": "A$"
    }
    symbol = symbols.get(currency, currency)
    return f"{symbol}{amount:.2f}"


def calculate_savings_percentage(original: float, discounted: float) -> float:
    """Calculate savings percentage between two amounts."""
    if original <= 0:
        return 0.0
    savings = ((original - discounted) / original) * 100
    return max(0, round(savings, 2))