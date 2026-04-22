from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import os
import json


class SummariserAgent:
    """Agent responsible for final itinerary summarization."""
    
    def __init__(self, temperature: float = 0.2):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
    
    def create_final_itinerary(self, research: Dict, budget: Dict, logistics: Dict) -> str:
        """
        Create a polished, human-readable itinerary.
        
        Args:
            research (Dict): Research findings.
            budget (Dict): Budget breakdown.
            logistics (Dict): Daily itinerary.
        
        Returns:
            str: Formatted itinerary text.
        """
        try:
            system_prompt = SystemMessage(
                content="You are a professional travel consultant. Create beautiful, detailed, location-specific itineraries."
            )
            
            destination = research.get("destination", "your destination")
            weather = research.get("weather", {}).get("forecast", [])
            weather_text = self._format_weather(weather)
            
            human_prompt = HumanMessage(
                content=f"""
                Create a final travel itinerary for {destination} using this data:
                
                RESEARCH: {json.dumps(research, indent=2)}
                BUDGET: {json.dumps(budget, indent=2)}
                LOGISTICS: {json.dumps(logistics, indent=2)}
                
                Format requirements:
                1. Start with "=== TRAVEL ITINERARY FOR {destination.upper()} ==="
                2. Include weather forecast section: {weather_text}
                3. For each day, show specific activities with attraction names
                4. Include budget breakdown with daily costs
                5. Add location-specific tips
                6. End with "Enjoy your trip to {destination}!"
                
                Make it detailed, specific to {destination}, and actionable.
                """
            )
            
            response = self.llm.invoke([system_prompt, human_prompt])
            
            return response.content.strip()
        
        except Exception as e:
            print(f"Summary generation error: {e}")
            return self._get_fallback_summary(research, budget, logistics)
    
    def _format_weather(self, weather_forecast: list) -> str:
        """Format weather forecast for prompt."""
        if not weather_forecast:
            return "Weather information not available"
        
        days = []
        for day in weather_forecast[:3]:
            days.append(f"{day.get('date', 'Unknown')}: {day.get('condition', 'Unknown')}, {day.get('max_temp', '?')}°C")
        
        return " | ".join(days)
    
    def _get_fallback_summary(self, research: Dict, budget: Dict, logistics: Dict) -> str:
        """Provide contextual fallback summary."""
        destination = research.get("destination", "your destination")
        days = logistics.get("days", 3)
        currency = budget.get("currency", "USD")
        
        summary = f"""
=== TRAVEL ITINERARY FOR {destination.upper()} ===

WEATHER FORECAST:
{research.get('weather', {}).get('forecast', [{}])[0].get('condition', 'Pleasant')} conditions expected during your stay.

DAILY ITINERARY:
"""
        
        itinerary = logistics.get("itinerary", [])
        for day in itinerary:
            summary += f"""
Day {day.get('day_number', '?')}: {day.get('theme', 'Exploration')}
  Morning: {day.get('morning_activity', 'Sightseeing')}
  Afternoon: {day.get('afternoon_activity', 'Local experiences')}
  Evening: {day.get('evening_activity', 'Dinner')}
  Meal Suggestion: {day.get('meals_suggestion', 'Local cuisine')}
"""
        
        breakdown = budget.get("breakdown", {})
        summary += f"""
BUDGET BREAKDOWN ({currency}):
  Daily Budget: {budget.get('daily_budget', 'N/A')}
  Accommodation: {breakdown.get('accommodation', 'N/A')}
  Food: {breakdown.get('food', 'N/A')}
  Activities: {breakdown.get('activities', 'N/A')}
  Transport: {breakdown.get('transport', 'N/A')}
  Miscellaneous: {breakdown.get('misc', 'N/A')}

LOCATION-SPECIFIC TIPS:
- Research local transportation options in {destination}
- Learn a few basic local phrases
- Check peak hours for popular attractions
- Carry local currency for small purchases
- Book popular restaurants in advance

Enjoy your trip to {destination}!
"""
        
        return summary