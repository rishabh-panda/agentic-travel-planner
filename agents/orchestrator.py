from typing import Dict, Any
from .research_agent import ResearchAgent
from .budget_agent import BudgetAgent
from .logistics_agent import LogisticsAgent
from .summariser_agent import SummariserAgent


class Orchestrator:
    """Orchestrates all agents to create a complete travel plan."""
    
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.budget_agent = BudgetAgent()
        self.logistics_agent = LogisticsAgent()
        self.summariser_agent = SummariserAgent()
    
    def create_travel_plan(self, destination: str, days: int, budget: float, 
                          currency: str, interests: str) -> Dict[str, Any]:
        """
        Execute the full travel planning pipeline.
        
        Args:
            destination (str): Travel destination.
            days (int): Number of days.
            budget (float): Total budget.
            currency (str): Currency code.
            interests (str): User interests.
        
        Returns:
            Dict[str, Any]: Complete travel plan.
        """
        try:
            # Step 1: Research
            print("Research Agent: Gathering destination information...")
            research = self.research_agent.research(destination, interests, days)
            
            if research.get("error"):
                print(f"Research warning: {research['error']}")
            
            # Step 2: Budget Planning
            print("Budget Agent: Calculating budget breakdown...")
            budget_plan = self.budget_agent.calculate_budget(budget, currency, days, destination)
            
            # Step 3: Logistics Planning
            print("Logistics Agent: Creating daily itinerary...")
            attractions = research.get("attractions", [])
            logistics = self.logistics_agent.plan_itinerary(attractions, days, destination, interests)
            
            # Step 4: Final Summary
            print("Summariser Agent: Generating final itinerary...")
            final_itinerary = self.summariser_agent.create_final_itinerary(
                research, budget_plan, logistics
            )
            
            return {
                "success": True,
                "research": research,
                "budget": budget_plan,
                "logistics": logistics,
                "final_itinerary": final_itinerary,
                "destination": destination,
                "days": days
            }
        
        except Exception as e:
            print(f"Orchestration error: {e}")
            return {
                "success": False,
                "error": str(e),
                "final_itinerary": f"Unable to create travel plan. Error: {str(e)}\n\nPlease check your inputs and try again."
            }