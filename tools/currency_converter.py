from typing import Dict, Optional
import requests
import os
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta


class CurrencyConverter:
    """Handles currency conversion with caching and fallback rates."""
    
    _instance = None
    _cache = {}
    _cache_expiry = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.api_key = os.getenv("EXCHANGE_RATE_API_KEY", "")
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
        # Dynamic fallback rates - will be updated from API on first use
        self.fallback_rates = {
            "USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 148.50,
            "CAD": 1.35, "AUD": 1.52, "INR": 83.50, "CNY": 7.20,
            "SGD": 1.34, "CHF": 0.91, "NZD": 1.65, "ZAR": 18.90,
            "BRL": 5.10, "RUB": 92.50, "KRW": 1350.00, "MXN": 16.80
        }
        self._last_update = None
    
    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert amount from one currency to another with caching."""
        if from_currency.upper() == to_currency.upper():
            return amount
        
        cache_key = f"{from_currency.upper()}_{to_currency.upper()}"
        
        # Check cache
        if cache_key in self._cache and self._cache_expiry.get(cache_key, datetime.min) > datetime.now():
            rate = self._cache[cache_key]
            converted = amount * rate
            return float(Decimal(str(converted)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        
        try:
            response = requests.get(f"{self.base_url}/{from_currency.upper()}", timeout=5)
            data = response.json()
            rate = data["rates"].get(to_currency.upper())
            
            if rate:
                # Cache for 1 hour
                self._cache[cache_key] = rate
                self._cache_expiry[cache_key] = datetime.now() + timedelta(hours=1)
                converted = amount * rate
                return float(Decimal(str(converted)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        except Exception as e:
            print(f"Currency conversion API error: {e}")
        
        # Fallback to approximate rates
        from_rate = self.fallback_rates.get(from_currency.upper(), 1.0)
        to_rate = self.fallback_rates.get(to_currency.upper(), 1.0)
        rate = to_rate / from_rate
        converted = amount * rate
        return float(Decimal(str(converted)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    
    def get_supported_currencies(self) -> list:
        """Return list of supported currencies."""
        return list(self.fallback_rates.keys())
    
    def get_rate(self, from_currency: str, to_currency: str) -> float:
        """Get exchange rate between two currencies."""
        return self.convert(1.0, from_currency, to_currency)