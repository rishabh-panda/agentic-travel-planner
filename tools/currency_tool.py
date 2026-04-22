from typing import Dict, Any
import requests


def convert_currency(amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
    """
    Convert currency using free API.
    
    Args:
        amount (float): Amount to convert.
        from_currency (str): Source currency code (USD, EUR, etc.).
        to_currency (str): Target currency code.
    
    Returns:
        Dict[str, Any]: Conversion result.
    """
    try:
        url = f"https://api.frankfurter.app/latest?from={from_currency.upper()}&to={to_currency.upper()}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return _get_fallback_conversion(amount, from_currency, to_currency)
        
        data = response.json()
        rate = data["rates"][to_currency.upper()]
        converted_amount = amount * rate
        
        return {
            "amount": amount,
            "from_currency": from_currency.upper(),
            "to_currency": to_currency.upper(),
            "converted_amount": round(converted_amount, 2),
            "rate": round(rate, 4),
            "source": "Frankfurter API (free)"
        }
    
    except Exception as e:
        print(f"Currency conversion error: {e}")
        return _get_fallback_conversion(amount, from_currency, to_currency)


def _get_fallback_conversion(amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
    """Provide fallback conversion rates."""
    fallback_rates = {
        ("USD", "EUR"): 0.92,
        ("EUR", "USD"): 1.09,
        ("USD", "GBP"): 0.79,
        ("GBP", "USD"): 1.27,
        ("USD", "JPY"): 149.50,
        ("JPY", "USD"): 0.0067
    }
    
    rate = fallback_rates.get((from_currency.upper(), to_currency.upper()), 1.0)
    
    return {
        "amount": amount,
        "from_currency": from_currency.upper(),
        "to_currency": to_currency.upper(),
        "converted_amount": round(amount * rate, 2),
        "rate": rate,
        "source": "Fallback rate (approximate)",
        "warning": "Using approximate exchange rate"
    }