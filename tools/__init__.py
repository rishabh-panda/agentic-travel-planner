from .search_tool import search_attractions
from .weather_tool import get_weather_forecast
from .currency_converter import CurrencyConverter
from .distance_tool import calculate_travel_time

# For backward compatibility, create a function wrapper
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Wrapper for currency conversion."""
    converter = CurrencyConverter()
    return converter.convert(amount, from_currency, to_currency)

__all__ = ['search_attractions', 'get_weather_forecast', 'convert_currency', 'calculate_travel_time', 'CurrencyConverter']