"""
Weather Data Fallback Component for Agentic Travel Planner
Implements friendly fallback with estimated weather based on season
"""

from typing import Dict, Any, Optional
from datetime import datetime


class WeatherFallback:
    """Manages weather data fallback and estimation"""
    
    def __init__(self):
        self.seasons = {
            "spring": [3, 4, 5],
            "summer": [6, 7, 8],
            "autumn": [9, 10, 11],
            "winter": [12, 1, 2]
        }
        
        self.weather_conditions = {
            "spring": ["Partly Cloudy", "Sunny", "Light Rain", "Mixed"],
            "summer": ["Sunny", "Partly Cloudy", "Hot", "Humid"],
            "autumn": ["Partly Cloudy", "Sunny", "Light Rain", "Cool"],
            "winter": ["Cloudy", "Light Snow", "Freezing Rain", "Cold"]
        }
    
    def get_season(self, month: int) -> str:
        """
        Determine season based on month.
        
        Args:
            month: Month number (1-12)
        
        Returns:
            Season name
        """
        for season, months in self.seasons.items():
            if month in months:
                return season
        return "spring"  # Default
    
    def estimate_weather(
        self,
        destination: str,
        season: str,
        days: int
    ) -> Dict[str, Any]:
        """
        Estimate weather based on destination and season.
        
        Args:
            destination: Destination name
            season: Season name
            days: Number of days
        
        Returns:
            Dictionary with estimated weather forecast
        """
        conditions = self.weather_conditions.get(season, ["Partly Cloudy"])
        
        # Generate estimated temperatures based on season
        base_temps = self._get_base_temperatures(season)
        
        forecast = []
        for day in range(days):
            condition = conditions[day % len(conditions)]
            temp = base_temps + (day % 3) - 1  # Slight variation
            
            forecast.append({
                "date": self._get_date_offset(day),
                "condition": condition,
                "temp": temp,
                "humidity": self._estimate_humidity(season),
                "wind_speed": self._estimate_wind(season),
                "is_estimated": True
            })
        
        return {
            "is_estimated": True,
            "season": season,
            "destination": destination,
            "forecast": forecast,
            "disclaimer": "Weather data not available. Estimated based on seasonal patterns."
        }
    
    def _get_base_temperatures(self, season: str) -> int:
        """
        Get base temperature for season.
        
        Args:
            season: Season name
        
        Returns:
            Base temperature in Celsius
        """
        base_temps = {
            "spring": 18,
            "summer": 28,
            "autumn": 15,
            "winter": 5
        }
        return base_temps.get(season, 18)
    
    def _estimate_humidity(self, season: str) -> int:
        """
        Estimate humidity based on season.
        
        Args:
            season: Season name
        
        Returns:
            Humidity percentage
        """
        humidities = {
            "spring": 60,
            "summer": 70,
            "autumn": 65,
            "winter": 55
        }
        return humidities.get(season, 60)
    
    def _estimate_wind(self, season: str) -> int:
        """
        Estimate wind speed based on season.
        
        Args:
            season: Season name
        
        Returns:
            Wind speed in km/h
        """
        winds = {
            "spring": 15,
            "summer": 10,
            "autumn": 18,
            "winter": 20
        }
        return winds.get(season, 15)
    
    def _get_date_offset(self, day_offset: int) -> str:
        """
        Get date string for day offset.
        
        Args:
            day_offset: Days from today
        
        Returns:
            Date string in YYYY-MM-DD format
        """
        date = datetime.now()
        # Simple implementation - in production, use proper date arithmetic
        return f"Day {day_offset + 1}"
    
    def get_fallback_html(self, estimated_weather: Dict[str, Any]) -> str:
        """
        Generate HTML for weather fallback message.
        
        Args:
            estimated_weather: Estimated weather data from estimate_weather
        
        Returns:
            HTML string for fallback message
        """
        season = estimated_weather.get("season", "unknown")
        disclaimer = estimated_weather.get("disclaimer", "")
        
        return f"""
        <div class="weather-fallback" style="
            background-color: #F0F9FF;
            border-left: 4px solid #008080;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        ">
            <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">🌤️</span>
                <div>
                    <strong style="color: #1E3A5F;">Weather Data Not Available</strong>
                    <p style="margin: 0.5rem 0 0.5rem 0; color: #1F2937;">{disclaimer}</p>
                    <p style="margin: 0; color: #6B7280;">
                        Based on {season} patterns for {estimated_weather.get('destination', 'this location')}:
                    </p>
                    <ul style="margin: 0.5rem 0; padding-left: 1.5rem; color: #1F2937;">
                        <li>Temperature: ~{self._get_base_temperatures(season)}°C</li>
                        <li>Conditions: {', '.join(self.weather_conditions.get(season, ['Partly Cloudy']))[:50]}...</li>
                        <li>Humidity: ~{self._estimate_humidity(season)}%</li>
                    </ul>
                </div>
            </div>
        </div>
        """
    
    def get_css(self) -> str:
        """
        Get CSS for weather fallback message.
        
        Returns:
            CSS string for styling
        """
        return """
        .weather-fallback {
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        """
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "seasons": self.seasons,
            "weather_conditions": self.weather_conditions
        }
