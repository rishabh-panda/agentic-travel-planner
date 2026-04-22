from typing import Dict, Any, List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os
import json

from tools import search_attractions, get_weather_forecast


class ResearchAgent:
    """Agent responsible for researching destination information."""
    
    def __init__(self, temperature: float = 0.3):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
    
    def research(self, destination: str, interests: str, days: int) -> Dict[str, Any]:
        """
        Research attractions and weather for destination.
        
        Args:
            destination (str): Travel destination.
            interests (str): User interests (comma-separated).
            days (int): Number of travel days.
        
        Returns:
            Dict[str, Any]: Research findings.
        """
        try:
            attractions = search_attractions(destination, limit=8)
            weather = get_weather_forecast(destination, days)
            
            if not attractions:
                raise ValueError("No attractions found")
            
            refined_attractions = self._refine_attractions(attractions, interests, destination)
            
            return {
                "destination": destination,
                "attractions": refined_attractions[:5],
                "weather": weather,
                "interests": interests
            }
        
        except Exception as e:
            print(f"Research error: {e}")
            return {
                "destination": destination,
                "attractions": attractions if 'attractions' in locals() else [],
                "weather": weather if 'weather' in locals() else {},
                "interests": interests,
                "error": str(e)
            }
    
    def _refine_attractions(self, attractions: List[Dict], interests: str, destination: str) -> List[Dict]:
        """Use LLM to filter attractions based on user interests."""
        try:
            prompt = f"""
            For the city {destination}, here are some attractions:
            {json.dumps(attractions, indent=2)}
            
            User interests: {interests}
            
            Return a JSON list of the top 5 attractions that best match these interests.
            Each item should have keys: name, description, and match_reason.
            """
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            
            content = response.content.strip()
            content = content.replace("```json", "").replace("```", "").strip()
            
            refined = json.loads(content)
            return refined if isinstance(refined, list) else attractions[:5]
        
        except Exception as e:
            print(f"Attraction refinement error: {e}")
            return attractions[:5]