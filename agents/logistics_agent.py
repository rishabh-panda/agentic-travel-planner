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
            attractions: List of attractions
            days: Number of days
            destination: Travel destination
            interests: User interests (string)
        
        Returns:
            Dict with daily itinerary in format expected by summariser
        """
        try:
            if not attractions:
                print("No attractions provided, using LLM-generated itinerary")
                return self._get_llm_fallback_itinerary(destination, days, interests)
            
            raw_itinerary = self._generate_itinerary(attractions, days, destination, interests)
            
            formatted_itinerary = self._format_for_summariser(raw_itinerary, days)
            
            return {
                "destination": destination,
                "days": days,
                "itinerary": formatted_itinerary,
                "total_attractions": len(attractions)
            }
        
        except Exception as e:
            print(f"Logistics planning error: {e}")
            return self._get_llm_fallback_itinerary(destination, days, interests)
    
    def _format_for_summariser(self, raw_itinerary: List[Dict], days: int) -> List[Dict]:
        """Convert logistics agent's itinerary format to summariser's expected format."""
        formatted = []
        
        for day in raw_itinerary[:days]:
            activities = []
            
            if day.get("morning_activity"):
                morning_value = day["morning_activity"]
                if " - " in morning_value:
                    parts = morning_value.split(" - ", 1)
                    activities.append({
                        "time": "Morning",
                        "name": parts[0].strip(),
                        "description": parts[1].strip()
                    })
                else:
                    activities.append({
                        "time": "Morning",
                        "name": morning_value,
                        "description": ""
                    })
            
            if day.get("afternoon_activity"):
                afternoon_value = day["afternoon_activity"]
                if " - " in afternoon_value:
                    parts = afternoon_value.split(" - ", 1)
                    activities.append({
                        "time": "Afternoon",
                        "name": parts[0].strip(),
                        "description": parts[1].strip()
                    })
                else:
                    activities.append({
                        "time": "Afternoon",
                        "name": afternoon_value,
                        "description": ""
                    })
            
            if day.get("evening_activity"):
                evening_value = day["evening_activity"]
                if " - " in evening_value:
                    parts = evening_value.split(" - ", 1)
                    activities.append({
                        "time": "Evening",
                        "name": parts[0].strip(),
                        "description": parts[1].strip()
                    })
                else:
                    activities.append({
                        "time": "Evening",
                        "name": evening_value,
                        "description": ""
                    })
            
            formatted.append({
                "theme": day.get("theme", "Explore"),
                "activities": activities,
                "meal_suggestions": day.get("meals_suggestion", day.get("meal_suggestions", "Local cuisine"))
            })
        
        return formatted
    
    def _generate_itinerary(self, attractions: List[Dict], days: int, destination: str, interests: str) -> List[Dict]:
        """Use LLM to generate daily schedule."""
        try:
            attractions_text = "\n".join([
                f"- {a['name']}: {a.get('description', 'No description available')}" 
                for a in attractions[:12]
            ])
            
            prompt = f"""
            You are a professional travel planner.
            Create a well-structured, realistic, and engaging {days}-day travel itinerary for {destination}.

            Traveler profile:
            - Interests: {interests}
            
            Available attractions in {destination}:
            {attractions_text}
            
            Instructions:
            - Use ONLY the provided attractions where possible, prioritizing relevance to the user's interests.
            - Distribute activities logically across {days} days (avoid clustering too many major attractions in one day).
            - Ensure geographical and practical feasibility (group nearby places together when possible).
            - Vary themes across days to create a balanced experience (culture, relaxation, exploration, food, etc.).
            - Keep activities concise but descriptive.

            Output format:
            Return ONLY a valid JSON array with exactly {days} objects (no extra text, no explanations).

            Each day object MUST include:
            - "day_number": integer (starting from 1)
            - "theme": short descriptive title for the day
            - "morning_activity": "Place Name - What makes it special"
            - "afternoon_activity": "Place Name - What makes it special"
            - "evening_activity": "Place Name - What makes it special"
            - "meals_suggestion": a short suggestion (local cuisine or dining area)

            CRITICAL FORMATTING RULES:
            - Each activity MUST strictly follow this format: "Place Name - What makes it special"
            - Use ONLY one dash (" - ") per activity.
            - Do NOT repeat or extend the description after the dash.
            - Keep descriptions concise (one short phrase).
            - Do NOT include markdown, code blocks, or explanations.
            - Ensure the output is valid JSON and directly parsable.

            Ensure the itinerary feels natural, diverse, and tailored specifically to {destination}.
            """
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            content = content.replace("```json", "").replace("```", "").strip()
            
            itinerary = json.loads(content)
            
            if isinstance(itinerary, list) and len(itinerary) == days:
                return itinerary
            else:
                return self._get_llm_fallback_itinerary(destination, days, interests)["itinerary"]
        
        except Exception as e:
            print(f"Itinerary generation error: {e}")
            return self._get_llm_fallback_itinerary(destination, days, interests)["itinerary"]
    
    def _get_llm_fallback_itinerary(self, destination: str, days: int, interests: str) -> Dict[str, Any]:
        """Generate a fallback itinerary using LLM only."""
        try:
            prompt = f"""
            Create a detailed {days}-day travel itinerary for {destination}.
            User interests include: {interests}.
            
            Return as a JSON list with exactly {days} days. Each day must have:
            - day_number (integer)
            - theme (string)
            - morning_activity (string with format "Activity Name - Brief description")
            - afternoon_activity (string with format "Activity Name - Brief description")
            - evening_activity (string with format "Activity Name - Brief description")
            - meals_suggestion (string)
            
            Use exactly this format: "Place Name - What makes it special"
            """
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            content = content.replace("```json", "").replace("```", "").strip()
            
            itinerary = json.loads(content)
            
            if isinstance(itinerary, list) and len(itinerary) == days:
                formatted_itinerary = self._format_for_summariser(itinerary, days)
                return {
                    "destination": destination,
                    "days": days,
                    "itinerary": formatted_itinerary,
                    "total_attractions": 0,
                    "warning": "Using LLM-generated itinerary"
                }
            else:
                raise ValueError("Invalid itinerary format")
                
        except Exception as e:
            print(f"LLM fallback error: {e}")
            formatted_itinerary = self._create_dynamic_fallback(destination, days, interests)
            return {
                "destination": destination,
                "days": days,
                "itinerary": formatted_itinerary,
                "total_attractions": 0,
                "warning": "Using dynamic fallback itinerary"
            }
    
    def _create_dynamic_fallback(self, destination: str, days: int, interests: str) -> List[Dict]:
        """Create a completely dynamic fallback itinerary."""
        itinerary = []
        
        day_themes = [
            f"Exploring {destination}",
            f"Culture and Cuisine in {destination}",
            f"Adventure in {destination}",
            f"Local Experience in {destination}",
            f"Discovery of {destination}"
        ]
        
        for day_num in range(1, days + 1):
            theme_idx = (day_num - 1) % len(day_themes)
            theme = day_themes[theme_idx]
            
            itinerary.append({
                "theme": theme,
                "activities": [
                    {"time": "Morning", "name": f"Morning exploration of {destination}", "description": f"Discover the best of {destination} starting your day"},
                    {"time": "Afternoon", "name": f"Afternoon activities in {destination}", "description": f"Continue exploring {destination} attractions"},
                    {"time": "Evening", "name": f"Evening experience in {destination}", "description": f"Enjoy the local nightlife and cuisine"}
                ],
                "meal_suggestions": f"Try local specialties at recommended restaurants in {destination}"
            })
        
        return itinerary