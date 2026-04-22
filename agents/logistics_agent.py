from typing import Dict, Any, List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os
import json


class LogisticsAgent:
    """Agent responsible for day-by-day planning."""
    
    def __init__(self, temperature: float = 0.3):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
    
    def plan_itinerary(self, attractions: List[Dict], days: int, destination: str, interests: str) -> Dict[str, Any]:
        """
        Create day-by-day itinerary.
        
        Args:
            attractions (List[Dict]): List of attractions.
            days (int): Number of days.
            destination (str): Travel destination.
            interests (str): User interests.
        
        Returns:
            Dict[str, Any]: Daily itinerary.
        """
        try:
            if not attractions:
                raise ValueError("No attractions to plan")
            
            itinerary = self._generate_itinerary(attractions, days, destination, interests)
            
            return {
                "destination": destination,
                "days": days,
                "itinerary": itinerary,
                "total_attractions": len(attractions)
            }
        
        except Exception as e:
            print(f"Logistics planning error: {e}")
            return self._get_fallback_itinerary(destination, days, interests)
    
    def _generate_itinerary(self, attractions: List[Dict], days: int, destination: str, interests: str) -> List[Dict]:
        """Use LLM to generate daily schedule."""
        try:
            attractions_text = "\n".join([f"- {a['name']}: {a.get('description', '')[:100]}" for a in attractions[:8]])
            
            prompt = f"""
            Create a detailed {days}-day itinerary for {destination}.
            User interests: {interests}
            
            Available attractions in {destination}:
            {attractions_text}
            
            Return as a JSON list with exactly {days} days. Each day must have:
            - day_number (integer)
            - theme (string, specific to activities)
            - morning_activity (specific attraction or activity with name)
            - afternoon_activity (specific attraction or activity with name)
            - evening_activity (specific restaurant type or entertainment)
            - meals_suggestion (specific local dish or restaurant type)
            
            Be specific and realistic for {destination}.
            """
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            content = content.replace("```json", "").replace("```", "").strip()
            
            itinerary = json.loads(content)
            
            if isinstance(itinerary, list) and len(itinerary) == days:
                return itinerary
            else:
                return self._get_fallback_itinerary(destination, days, interests)["itinerary"]
        
        except Exception as e:
            print(f"Itinerary generation error: {e}")
            return self._get_fallback_itinerary(destination, days, interests)["itinerary"]
    
    def _get_fallback_itinerary(self, destination: str, days: int, interests: str) -> Dict[str, Any]:
        """Provide contextual fallback itinerary based on destination and interests."""
        itinerary = []
        
        for day in range(1, days + 1):
            if day == 1:
                theme = "Arrival and Introduction"
                morning = f"Check into accommodation and explore {destination} city center"
                afternoon = f"Visit local markets and try street food in {destination}"
                evening = f"Welcome dinner at a popular {self._get_cuisine_type(interests)} restaurant"
            elif day == days:
                theme = "Last Day Highlights"
                morning = f"Visit top attraction in {destination}"
                afternoon = f"Last minute souvenir shopping in {destination}"
                evening = f"Farewell dinner at a highly-rated local spot"
            else:
                theme = f"Exploring {destination} Culture"
                morning = f"Visit museums and historical sites in {destination}"
                afternoon = f"Food tour experiencing local {self._get_cuisine_type(interests)} cuisine"
                evening = f"{self._get_nightlife(interests)} in {destination}"
            
            itinerary.append({
                "day_number": day,
                "theme": theme,
                "morning_activity": morning,
                "afternoon_activity": afternoon,
                "evening_activity": evening,
                "meals_suggestion": f"Try {self._get_local_dish(destination)}"
            })
        
        return {
            "destination": destination,
            "days": days,
            "itinerary": itinerary,
            "total_attractions": 0,
            "warning": "Using contextual fallback itinerary"
        }
    
    def _get_cuisine_type(self, interests: str) -> str:
        """Extract cuisine interest from user input."""
        if "food" in interests.lower() or "street food" in interests.lower():
            return "local street food"
        elif "fine dining" in interests.lower():
            return "fine dining"
        else:
            return "traditional"
    
    def _get_nightlife(self, interests: str) -> str:
        """Extract nightlife interest."""
        if "clubbing" in interests.lower():
            return "Experience nightlife and clubs"
        elif "bars" in interests.lower():
            return "Visit popular bars and lounges"
        else:
            return "Relaxing evening walk"
    
    def _get_local_dish(self, destination: str) -> str:
        """Suggest local dish based on destination."""
        local_dishes = {
            "gurugram": "butter chicken and naan",
            "paris": "croissants and escargot",
            "tokyo": "sushi and ramen",
            "new york": "pizza and bagels",
            "london": "fish and chips",
            "mumbai": "vada pav and pav bhaji"
        }
        
        destination_lower = destination.lower()
        for key in local_dishes:
            if key in destination_lower:
                return local_dishes[key]
        
        return "local specialties"