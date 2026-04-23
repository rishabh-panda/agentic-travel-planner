from typing import List, Dict, Any


class SummariserAgent:
    def create_final_itinerary(self, research: Dict, budget_info: Dict, logistics: Dict) -> str:
        """Create final itinerary from all agent outputs."""
        destination = research.get("destination", "Unknown")
        days = research.get("days", logistics.get("days", 3))
        weather = research.get("weather", {"forecast": []})
        daily_plan = logistics.get("itinerary", [])
        
        return self.generate_final_itinerary(
            destination=destination,
            days=days,
            budget_info=budget_info,
            daily_plan=daily_plan,
            weather=weather,
            interests=[],
            logistics=logistics
        )
    
    def generate_final_itinerary(self, destination: str, days: int, budget_info: Dict, 
                                  daily_plan: List[Dict], weather: Dict, interests: List[str],
                                  logistics: Dict = None) -> str:
        """Generate readable itinerary from all agent outputs."""
        output = []
        output.append(f"=== TRAVEL ITINERARY FOR {destination.upper()} ===\n")
        
        output.append("**Weather Forecast:**")
        forecast_list = weather.get("forecast", [])
        if forecast_list:
            for day in forecast_list:
                date = day.get('date', 'Unknown')
                condition = day.get('condition', 'Unknown')
                temp = day.get('temp', 'N/A')
                output.append(f"{date}: {condition}, {temp}°C")
        else:
            output.append("Weather data not available")
        output.append("")
        
        for day_idx, plan in enumerate(daily_plan, 1):
            theme = plan.get('theme', f'Day {day_idx}')
            output.append(f"**Day {day_idx}:** {theme}")
            
            activities = plan.get("activities", [])
            if activities:
                for activity in activities:
                    time = activity.get('time', '')
                    name = activity.get('name', '')
                    description = activity.get('description', '')
                    if name and description:
                        output.append(f"- {time}: {name} - {description}")
                    elif name:
                        output.append(f"- {time}: {name}")
            else:
                if plan.get('morning_activity'):
                    output.append(f"- Morning: {plan.get('morning_activity')}")
                if plan.get('afternoon_activity'):
                    output.append(f"- Afternoon: {plan.get('afternoon_activity')}")
                if plan.get('evening_activity'):
                    output.append(f"- Evening: {plan.get('evening_activity')}")
            
            meals = plan.get('meal_suggestions', plan.get('meals_suggestion', 'Local cuisine'))
            output.append(f"- Meals: {meals}")
            output.append("")
        
        output.append("**Budget Breakdown:**")
        output.append(f"- Total Budget: {budget_info.get('currency', 'USD')} {budget_info.get('total_budget', 0)}")
        output.append(f"- Daily Budget: {budget_info.get('currency', 'USD')} {budget_info.get('daily_budget', 0)}")
        output.append("- Breakdown:")
        
        breakdown = budget_info.get("breakdown", {})
        for cat, amt in breakdown.items():
            output.append(f"  - {cat.capitalize()}: {budget_info.get('currency', 'USD')} {amt}")
        
        quality = budget_info.get("quality_warning", {})
        risk_level = quality.get("risk_level", "")
        message = quality.get("message", "")
        suggested_action = quality.get("suggested_action", "")
        
        if risk_level in ["high", "critical", "medium"] and message:
            output.append(f"\n**Budget Quality Alert:** {message}")
            if suggested_action:
                output.append(f"**Recommendation:** {suggested_action}")
        
        hidden = budget_info.get("hidden_costs", [])
        if hidden:
            output.append("\n**Potential Hidden Costs to Avoid:**")
            for h in hidden[:3]:
                output.append(f"- {h.get('category', 'Unknown')}: {h.get('avoidance_tip', '')}")
        
        recs = budget_info.get("recommendations", [])
        if recs:
            output.append("\n**Recommendations:**")
            for r in recs[:3]:
                output.append(f"- {r}")
        
        if logistics and logistics.get("warning"):
            output.append(f"\n**Note:** {logistics.get('warning')}")
        
        output.append(f"\nEnjoy your trip to {destination}!")
        return "\n".join(output)