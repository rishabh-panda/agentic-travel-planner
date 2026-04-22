from typing import Dict, Any, List
import requests
from datetime import datetime, timedelta


def get_weather_forecast(city: str, days: int = 5) -> Dict[str, Any]:
    """
    Get weather forecast for a city.
    
    Args:
        city (str): City name.
        days (int): Number of days forecast.
    
    Returns:
        Dict[str, Any]: Weather forecast data.
    """
    try:
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_response = requests.get(geocode_url, timeout=10)
        
        if geo_response.status_code != 200:
            return _get_fallback_weather(city)
        
        geo_data = geo_response.json()
        
        if not geo_data.get("results"):
            return _get_fallback_weather(city)
        
        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto&forecast_days={days}"
        
        weather_response = requests.get(weather_url, timeout=10)
        
        if weather_response.status_code != 200:
            return _get_fallback_weather(city)
        
        weather_data = weather_response.json()
        
        forecast = []
        for i in range(days):
            forecast.append({
                "date": weather_data["daily"]["time"][i],
                "max_temp": weather_data["daily"]["temperature_2m_max"][i],
                "min_temp": weather_data["daily"]["temperature_2m_min"][i],
                "condition": _get_weather_condition(weather_data["daily"]["weathercode"][i])
            })
        
        return {
            "city": city,
            "forecast": forecast,
            "source": "Open-Meteo (free)"
        }
    
    except Exception as e:
        print(f"Weather error: {e}")
        return _get_fallback_weather(city)


def _get_weather_condition(code: int) -> str:
    """Convert weather code to readable condition."""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        51: "Light drizzle",
        61: "Rain",
        71: "Snow",
        95: "Thunderstorm"
    }
    return weather_codes.get(code, "Unknown")


def _get_fallback_weather(city: str) -> Dict[str, Any]:
    """Provide fallback weather data."""
    today = datetime.now()
    forecast = []
    
    for i in range(5):
        forecast.append({
            "date": (today + timedelta(days=i)).strftime("%Y-%m-%d"),
            "max_temp": 22,
            "min_temp": 15,
            "condition": "Partly cloudy"
        })
    
    return {
        "city": city,
        "forecast": forecast,
        "source": "Fallback data",
        "warning": "Using approximate weather data"
    }