import os
import json
import re
from typing import List, Dict, Any, Union
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from tools.search_tool import search_attractions
from tools.weather_tool import get_weather_forecast
from utils.helpers import load_config


class ResearchAgent:
    def __init__(self, temperature: float = 0.2, config_path: str = "config/budget_config.yaml"):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.config = load_config(config_path)  # ADD THIS LINE
        self._debug_printed = False

    def research(self, destination: str, interests: str, days: int) -> Dict[str, Any]:
        """Main research method called by orchestrator."""
        if isinstance(interests, str):
            interests_list = [i.strip().lower() for i in interests.replace(",", " ").split() if i.strip()]
        else:
            interests_list = interests
        
        result = self.get_destination_info(destination, interests_list)
        result["days"] = days
        result["interests"] = interests_list
        result["weather"] = self._parse_weather(result.get("weather", {}))
        
        return result

    def get_destination_info(self, destination: str, interests: List[str]) -> Dict[str, Any]:
        """Get weather and attractions for destination."""
        # Get forecast days from config, default to 3, ensure it's an integer
        forecast_days_config = self.config.get("weather", {}).get("forecast_days", 3)
        
        # Ensure forecast_days is an integer (not a list)
        if isinstance(forecast_days_config, list):
            forecast_days = forecast_days_config[0] if forecast_days_config else 3
        else:
            forecast_days = int(forecast_days_config) if forecast_days_config else 3
        
        # Cap at 7 days (API limit) and at least 1 day
        forecast_days = max(1, min(forecast_days, 7))
        
        weather = get_weather_forecast(destination, days=forecast_days)
        attractions = self._get_attractions(destination, interests)
        return {
            "destination": destination,
            "weather": weather,
            "attractions": attractions
        }

    def _parse_weather(self, weather_data: Union[Dict, List, Any]) -> Dict[str, Any]:
        """Parse raw weather data into format expected by summariser."""
        forecast = []
        
        if isinstance(weather_data, list):
            for idx, day in enumerate(weather_data[:3]):
                if isinstance(day, dict):
                    forecast.append({
                        "date": day.get("date", day.get("datetime", f"Day {idx+1}")),
                        "condition": self._extract_condition(day),
                        "temp": self._extract_temperature(day)
                    })
        
        elif isinstance(weather_data, dict):
            if "forecast" in weather_data:
                fdata = weather_data["forecast"]
                if isinstance(fdata, list):
                    for idx, day in enumerate(fdata[:3]):
                        forecast.append({
                            "date": day.get("date", day.get("datetime", f"Day {idx+1}")),
                            "condition": self._extract_condition(day),
                            "temp": self._extract_temperature(day)
                        })
                elif isinstance(fdata, dict) and "forecastday" in fdata:
                    for day in fdata["forecastday"][:3]:
                        forecast.append({
                            "date": day.get("date", "Unknown"),
                            "condition": day.get("day", {}).get("condition", {}).get("text", "Unknown"),
                            "temp": day.get("day", {}).get("avgtemp_c", day.get("day", {}).get("temp", "N/A"))
                        })
            
            elif "list" in weather_data:
                for day in weather_data["list"][:3]:
                    temp_val = day.get("main", {}).get("temp", "N/A")
                    if isinstance(temp_val, (int, float)):
                        temp_val = round(temp_val - 273.15, 1) if temp_val > 100 else temp_val
                    forecast.append({
                        "date": day.get("dt_txt", "Unknown")[:10],
                        "condition": day.get("weather", [{}])[0].get("description", "Unknown"),
                        "temp": temp_val
                    })
            
            elif "current" in weather_data:
                temp_val = weather_data.get("current", {}).get("temp_c", weather_data.get("current", {}).get("temp", "N/A"))
                if isinstance(temp_val, (int, float)) and temp_val > 100:
                    temp_val = round(temp_val - 273.15, 1)
                forecast.append({
                    "date": "Today",
                    "condition": weather_data.get("current", {}).get("condition", {}).get("text", "Unknown"),
                    "temp": temp_val
                })
            
            elif "daily" in weather_data:
                for day in weather_data["daily"][:3]:
                    forecast.append({
                        "date": day.get("dt", "Unknown"),
                        "condition": day.get("weather", [{}])[0].get("description", "Unknown"),
                        "temp": day.get("temp", {}).get("day", "N/A")
                    })
        
        if not forecast:
            forecast = [
                {"date": "Day 1", "condition": "Weather data unavailable", "temp": "N/A"},
                {"date": "Day 2", "condition": "Weather data unavailable", "temp": "N/A"},
                {"date": "Day 3", "condition": "Weather data unavailable", "temp": "N/A"}
            ]
        
        return {"forecast": forecast}
    
    def _extract_condition(self, day_data: Dict) -> str:
        """Extract weather condition from various API formats."""
        if "condition" in day_data:
            if isinstance(day_data["condition"], dict):
                return day_data["condition"].get("text", day_data["condition"].get("description", "Unknown"))
            return str(day_data["condition"])
        if "weather" in day_data and isinstance(day_data["weather"], list):
            return day_data["weather"][0].get("description", "Unknown")
        if "summary" in day_data:
            return day_data["summary"]
        return "Unknown"
    
    def _extract_temperature(self, day_data: Dict) -> Union[float, str]:
        """Extract temperature from various API formats."""
        if not self._debug_printed:
            print(f"Weather data keys: {list(day_data.keys()) if isinstance(day_data, dict) else type(day_data)}")
            self._debug_printed = True
        
        temp_fields = ["temp", "temperature", "avgtemp_c", "temp_c", "daytemp", "maxtemp", "max_temp", "min_temp", "feels_like", "avg_temp"]
        for field in temp_fields:
            if field in day_data:
                val = day_data[field]
                if isinstance(val, (int, float)):
                    return val if val < 100 else round(val - 273.15, 1)
                if isinstance(val, str) and val.replace('.', '').replace('-', '').isdigit():
                    return float(val)
        
        if "day" in day_data and isinstance(day_data["day"], dict):
            for field in temp_fields:
                if field in day_data["day"]:
                    val = day_data["day"][field]
                    if isinstance(val, (int, float)):
                        return val if val < 100 else round(val - 273.15, 1)
        
        if "main" in day_data and isinstance(day_data["main"], dict):
            if "temp" in day_data["main"]:
                val = day_data["main"]["temp"]
                return val if val < 100 else round(val - 273.15, 1)
        
        if "temperature" in day_data and isinstance(day_data["temperature"], dict):
            if "c" in day_data["temperature"]:
                return day_data["temperature"]["c"]
        
        return "N/A"

    def _get_attractions(self, destination: str, interests: List[str]) -> List[Dict[str, Any]]:
        """Fetch and refine attractions using LLM with robust JSON parsing."""
        raw_attractions = search_attractions(destination, interests)
        refined = self._refine_attractions_with_llm(destination, interests, raw_attractions)
        return refined

    def _refine_attractions_with_llm(self, destination: str, interests: List[str], raw_attractions: List[Dict]) -> List[Dict]:
        """Call LLM to refine attraction list and parse JSON robustly."""
        interests_str = ', '.join(interests)
        
        prompt = f"""
        You are a travel expert. Given the destination "{destination}" and user interests: {interests_str}.
        Here are some raw attraction suggestions: {json.dumps(raw_attractions)}.
        
        Refine and return a JSON list of objects, each with keys: "name", "description", "category", "estimated_hours", "price_level".
        The category must be one of: {interests_str}.
        The description should be a meaningful 1-2 sentence explanation.
        Return ONLY valid JSON, no other text.
        """
        
        max_retries = 2
        for attempt in range(max_retries + 1):
            try:
                response = self.llm.invoke([HumanMessage(content=prompt)])
                content = response.content.strip()
                content = re.sub(r'```json\s*', '', content)
                content = re.sub(r'```\s*', '', content)
                
                if not content:
                    raise ValueError("Empty response from LLM")
                
                attractions = json.loads(content)
                if isinstance(attractions, list) and len(attractions) > 0:
                    return attractions
                else:
                    raise ValueError("Not a valid list")
                    
            except Exception as e:
                print(f"Attraction refinement error (attempt {attempt+1}): {e}")
                if attempt == max_retries:
                    return self._fallback_attractions(raw_attractions, interests)
        return []

    def _fallback_attractions(self, raw: List[Dict], interests: List[str]) -> List[Dict]:
        """Provide fallback attractions when LLM fails."""
        fallback = []
        for idx, item in enumerate(raw[:12]):
            category = interests[idx % len(interests)] if interests else "general"
            fallback.append({
                "name": item.get("name", f"Attraction {idx+1}"),
                "description": item.get("description", f"Popular attraction in this destination"),
                "category": category,
                "estimated_hours": 2,
                "price_level": "mid"
            })
        return fallback