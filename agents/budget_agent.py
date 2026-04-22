from typing import Dict, Any
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os
import json

from tools import convert_currency


class BudgetAgent:
    """Agent responsible for budget planning."""
    
    SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "INR", "CNY", "SGD"]
    
    def __init__(self, temperature: float = 0.2):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
    
    def calculate_budget(self, total_budget: float, currency: str, days: int, destination: str) -> Dict[str, Any]:
        """
        Calculate daily budget breakdown.
        
        Args:
            total_budget (float): Total budget amount.
            currency (str): Currency code.
            days (int): Number of days.
            destination (str): Travel destination.
        
        Returns:
            Dict[str, Any]: Budget breakdown.
        """
        try:
            if currency.upper() not in self.SUPPORTED_CURRENCIES:
                return self._get_unsupported_currency_budget(total_budget, currency, days, destination)
            
            daily_budget = total_budget / days
            
            breakdown = self._get_llm_breakdown(daily_budget, days, destination, currency)
            
            return {
                "total_budget": total_budget,
                "currency": currency.upper(),
                "days": days,
                "daily_budget": round(daily_budget, 2),
                "breakdown": breakdown,
                "destination": destination
            }
        
        except Exception as e:
            print(f"Budget calculation error: {e}")
            return self._get_fallback_budget(total_budget, currency, days, destination)
    
    def _get_llm_breakdown(self, daily_budget: float, days: int, destination: str, currency: str) -> Dict[str, float]:
        """Use LLM to suggest budget allocation."""
        try:
            prompt = f"""
            For a trip to {destination} with a daily budget of {daily_budget:.2f} {currency} per day for {days} days,
            provide a realistic budget breakdown in JSON format with these categories: accommodation, food, activities, transport, misc.
            Each value should be a daily amount in {currency}.
            Consider typical costs in {destination}.
            """
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            content = response.content.strip()
            content = content.replace("```json", "").replace("```", "").strip()
            
            breakdown = json.loads(content)
            
            return breakdown
        
        except Exception as e:
            print(f"LLM budget breakdown error: {e}")
            return self._get_fallback_breakdown(daily_budget, currency)
    
    def _get_fallback_budget(self, total_budget: float, currency: str, days: int, destination: str) -> Dict[str, Any]:
        """Provide fallback budget calculation."""
        daily_budget = total_budget / days
        
        return {
            "total_budget": total_budget,
            "currency": currency.upper(),
            "days": days,
            "daily_budget": round(daily_budget, 2),
            "breakdown": self._get_fallback_breakdown(daily_budget, currency),
            "destination": destination,
            "warning": "Using estimated budget breakdown"
        }
    
    def _get_fallback_breakdown(self, daily_budget: float, currency: str) -> Dict[str, float]:
        """Provide fallback budget allocation."""
        return {
            "accommodation": round(daily_budget * 0.40, 2),
            "food": round(daily_budget * 0.25, 2),
            "activities": round(daily_budget * 0.20, 2),
            "transport": round(daily_budget * 0.10, 2),
            "misc": round(daily_budget * 0.05, 2)
        }
    
    def _get_unsupported_currency_budget(self, total_budget: float, currency: str, days: int, destination: str) -> Dict[str, Any]:
        """Handle unsupported currencies."""
        return {
            "total_budget": total_budget,
            "currency": currency.upper(),
            "days": days,
            "daily_budget": round(total_budget / days, 2),
            "breakdown": self._get_fallback_breakdown(total_budget / days, currency),
            "destination": destination,
            "warning": f"Currency {currency} not fully supported. Using approximate values.",
            "supported_currencies": self.SUPPORTED_CURRENCIES
        }