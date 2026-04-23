from typing import Dict, Any, Optional, List
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import os
import json
import yaml
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from tools.currency_converter import CurrencyConverter
from tools.cost_analyzer import CostAnalyzer
from tools.price_predictor import PricePredictor
from tools.quality_checker import QualityChecker
from models.budget_models import (
    BudgetRequest, BudgetResponse, BudgetBreakdown, 
    HiddenCostWarning, GroupBudgetProfile, RiskAssessment
)
from models.cost_constants import (
    HIDDEN_COST_CATEGORIES, QUALITY_THRESHOLDS,
    RISK_FACTORS, DEFAULT_ALLOCATION_PERCENTAGES
)
from utils.validators import validate_budget_input, validate_currency
from utils.helpers import load_config
from utils.validators import round_decimal


class BudgetAgent:
    
    def __init__(self, temperature: float = 0.2, config_path: str = "config/budget_config.yaml"):
        self.config = load_config(config_path)
        self.llm = ChatGroq(
            model=self.config.get("llm_model", "llama-3.3-70b-versatile"),
            temperature=temperature,
            api_key=os.getenv("GROQ_API_KEY")
        )
        self.currency_converter = CurrencyConverter()
        self.cost_analyzer = CostAnalyzer()
        self.price_predictor = PricePredictor()
        self.quality_checker = QualityChecker()
    
    def calculate_budget(self, total_budget=None, currency=None, days=None, destination=None, traveller_type=None, **kwargs):
        if isinstance(total_budget, dict):
            request = total_budget
        else:
            request = {
                "total_budget": total_budget,
                "currency": currency or "USD",
                "days": days,
                "destination": destination,
                "traveller_type": traveller_type or "mid-range",
                "group_size": kwargs.get("group_size", 1),
                "booking_window_days": kwargs.get("booking_window_days", 60),
                "include_hidden_costs": kwargs.get("include_hidden_costs", True),
                "risk_tolerance": kwargs.get("risk_tolerance", "medium"),
                "travel_style_priorities": kwargs.get("travel_style_priorities", [])
            }
        return self._calculate_budget_impl(request)
    
    def _calculate_budget_impl(self, request: Dict[str, Any]) -> Dict[str, Any]:
        validated_request = validate_budget_input(request)
        
        user_currency = validated_request["currency"]
        total_budget_user = validated_request["total_budget"]
        days = validated_request["days"]
        destination = validated_request["destination"]
        traveller_type = validated_request["traveller_type"]
        
        daily_budget_user = total_budget_user / days
        
        base_currency = self.config.get("base_currency", "USD")
        converted_budget_usd, conversion_rate = self._normalize_currency(
            total_budget_user, user_currency, base_currency
        )
        daily_budget_usd = converted_budget_usd / days
        
        hidden_costs = self._detect_hidden_costs(destination, traveller_type, days, user_currency)
        true_daily_cost_user = daily_budget_user + sum(hc["estimated_cost"] for hc in hidden_costs)
        
        quality_risk = self.quality_checker.assess_quality_risk(
            destination, daily_budget_usd, traveller_type, user_currency, daily_budget_user
        )
        
        surge_risk = self.price_predictor.assess_surge_risk(destination, validated_request["booking_window_days"])
        
        breakdown = self._generate_breakdown(
            daily_budget_user, days, destination, user_currency, traveller_type,
            validated_request["travel_style_priorities"]
        )
        
        deferred_risks = self._assess_deferred_purchase_risks(destination, validated_request["risk_tolerance"])
        
        group_profile = None
        if validated_request["group_size"] > 1:
            group_profile = self._generate_group_profile(validated_request["group_size"], daily_budget_user, breakdown)
        
        return {
            "total_budget": total_budget_user,
            "currency": user_currency,
            "days": days,
            "daily_budget": round_decimal(daily_budget_user, 2),
            "true_daily_cost": round_decimal(true_daily_cost_user, 2),
            "destination": destination,
            "traveller_type": traveller_type,
            "breakdown": breakdown,
            "hidden_costs": hidden_costs,
            "quality_warning": quality_risk,
            "surge_risk": surge_risk,
            "deferred_purchase_risks": deferred_risks,
            "group_profile": group_profile,
            "recommendations": self._generate_recommendations(quality_risk, surge_risk, deferred_risks, hidden_costs)
        }
    
    def calculate_group_budget_alignment(self, budgets: List[float], currency: str) -> Dict[str, Any]:
        if len(budgets) < 2:
            return {"warning": "Group alignment requires at least 2 travellers"}
        
        min_budget = min(budgets)
        max_budget = max(budgets)
        avg_budget = sum(budgets) / len(budgets)
        disparity_ratio = max_budget / min_budget if min_budget > 0 else float('inf')
        
        budget_tiers = {
            "budget": [b for b in budgets if b < avg_budget * 0.7],
            "mid_range": [b for b in budgets if avg_budget * 0.7 <= b <= avg_budget * 1.3],
            "luxury": [b for b in budgets if b > avg_budget * 1.3]
        }
        
        recommendations = []
        if disparity_ratio > 1.5:
            recommendations.append({
                "issue": "Significant budget disparity detected",
                "suggestion": "Consider splitting activities into separate groups or alternating expensive/affordable days",
                "compromise_activities": self._find_compromise_activities(avg_budget, currency)
            })
        
        if len(budget_tiers["luxury"]) > 0 and len(budget_tiers["budget"]) > 0:
            recommendations.append({
                "issue": "Mixing luxury and budget travellers",
                "suggestion": "Luxury travellers can subsidize shared accommodation or prepay for group activities",
                "expected_resolution": "Pre-discuss expectations before booking anything"
            })
        
        return {
            "total_travellers": len(budgets),
            "min_budget": min_budget,
            "max_budget": max_budget,
            "average_budget": avg_budget,
            "disparity_ratio": round(disparity_ratio, 2),
            "budget_tiers": {k: len(v) for k, v in budget_tiers.items()},
            "conflict_risk": "high" if disparity_ratio > 1.5 else "medium" if disparity_ratio > 1.2 else "low",
            "recommendations": recommendations
        }
    
    def calculate_true_cost(self, listed_price: float, currency: str, destination: str) -> Dict[str, Any]:
        hidden_cost_multipliers = {
            "flight": {"baggage": 0.15, "seat_selection": 0.05, "airport_transfer": 0.10},
            "hotel": {"resort_fee": 0.20, "parking": 0.08, "taxes": 0.12},
            "car_rental": {"insurance": 0.25, "fuel": 0.10, "additional_driver": 0.05}
        }
        
        category = self._detect_purchase_category(listed_price, destination)
        multipliers = hidden_cost_multipliers.get(category, {})
        
        hidden_total = listed_price * sum(multipliers.values())
        true_cost = listed_price + hidden_total
        
        return {
            "listed_price": listed_price,
            "currency": currency,
            "category": category,
            "hidden_costs_estimate": round(hidden_total, 2),
            "true_cost": round(true_cost, 2),
            "percentage_increase": round((hidden_total / listed_price) * 100, 2),
            "breakdown": {k: round(listed_price * v, 2) for k, v in multipliers.items()}
        }
    
    def assess_deferred_purchase_risk(self, item_type: str, item_cost: float, days_to_travel: int) -> Dict[str, Any]:
        risk_factors = RISK_FACTORS.get(item_type, {})
        
        if days_to_travel <= risk_factors.get("last_minute_threshold", 7):
            urgency = "critical"
            price_multiplier = risk_factors.get("last_minute_multiplier", 1.5)
        elif days_to_travel <= risk_factors.get("medium_window", 30):
            urgency = "high"
            price_multiplier = risk_factors.get("medium_multiplier", 1.2)
        else:
            urgency = "low"
            price_multiplier = 1.0
        
        estimated_deferred_cost = item_cost * price_multiplier
        additional_cost = estimated_deferred_cost - item_cost
        
        return {
            "item_type": item_type,
            "current_price": item_cost,
            "estimated_deferred_price": round(estimated_deferred_cost, 2),
            "additional_cost_if_deferred": round(additional_cost, 2),
            "urgency_level": urgency,
            "recommendation": "Book now" if urgency in ["critical", "high"] else "Can defer",
            "risk_factors": risk_factors.get("risks", [])
        }
    
    def generate_realtime_spending_alert(self, spent: float, category: str, daily_limit: float) -> Dict[str, Any]:
        percentage_used = (spent / daily_limit) * 100
        
        if percentage_used >= 100:
            alert_level = "critical"
            message = f"You have exceeded your {category} budget for today."
        elif percentage_used >= 80:
            alert_level = "warning"
            message = f"You have used {percentage_used:.0f}% of your {category} budget. {daily_limit - spent:.2f} remaining."
        elif percentage_used >= 60:
            alert_level = "info"
            message = f"You have used {percentage_used:.0f}% of your {category} budget."
        else:
            alert_level = "ok"
            message = f"On track with {category} spending."
        
        return {
            "category": category,
            "spent": round(spent, 2),
            "daily_limit": round(daily_limit, 2),
            "remaining": round(daily_limit - spent, 2),
            "percentage_used": round(percentage_used, 2),
            "alert_level": alert_level,
            "message": message
        }
    
    def _normalize_currency(self, amount: float, from_currency: str, to_currency: str) -> tuple:
        if from_currency.upper() == to_currency:
            return amount, 1.0
        converted = self.currency_converter.convert(amount, from_currency, to_currency)
        rate = converted / amount if amount > 0 else 1.0
        return converted, rate
    
    def _detect_hidden_costs(self, destination: str, traveller_type: str, days: int, currency: str) -> List[Dict]:
        hidden_costs = []
        
        for category, details in HIDDEN_COST_CATEGORIES.items():
            if details.get("applicable_to", ["all"]) == ["all"] or traveller_type in details.get("applicable_to", []):
                base_cost_usd = details.get("base_cost", 0)
                converted_cost = self.currency_converter.convert(base_cost_usd, "USD", currency)
                cost_estimate = converted_cost * days
                
                hidden_costs.append({
                    "category": category,
                    "description": details.get("description", ""),
                    "estimated_cost": round_decimal(cost_estimate, 2),
                    "avoidance_tip": details.get("avoidance_tip", ""),
                    "typical_impact": details.get("typical_impact", "medium")
                })
        
        return hidden_costs
    
    def _generate_breakdown(self, daily_budget: float, days: int, destination: str, 
                           currency: str, traveller_type: str, priorities: List[str]) -> Dict[str, float]:
        try:
            base_allocation = DEFAULT_ALLOCATION_PERCENTAGES.get(traveller_type, DEFAULT_ALLOCATION_PERCENTAGES["mid-range"])
            adjusted_percentages = self._adjust_for_priorities(base_allocation.copy(), priorities)
            
            initial_amounts = {}
            for cat, pct in adjusted_percentages.items():
                initial_amounts[cat] = daily_budget * (pct / 100.0)
            
            destination_adjustments = self.cost_analyzer.get_cost_adjustments(destination, traveller_type)
            adjusted_amounts = {}
            for cat, amount in initial_amounts.items():
                multiplier = destination_adjustments.get(cat, 1.0)
                adjusted_amounts[cat] = amount * multiplier
            
            total_adjusted = sum(adjusted_amounts.values())
            if abs(total_adjusted - daily_budget) > 0.01:
                scale_factor = daily_budget / total_adjusted
                for cat in adjusted_amounts:
                    adjusted_amounts[cat] = adjusted_amounts[cat] * scale_factor
            
            breakdown = {cat: round_decimal(amt, 2) for cat, amt in adjusted_amounts.items()}
            
            misc_pct = (breakdown.get("misc", 0) / daily_budget) * 100 if daily_budget > 0 else 0
            if misc_pct > 20:
                excess = breakdown["misc"] - (daily_budget * 0.10)
                if excess > 0:
                    breakdown["misc"] = daily_budget * 0.10
                    breakdown["accommodation"] += excess * 0.6
                    breakdown["food"] += excess * 0.4
                    for cat in ["accommodation", "food", "misc"]:
                        breakdown[cat] = round_decimal(breakdown[cat], 2)
            
            return breakdown
            
        except Exception as e:
            print(f"Breakdown generation error: {e}")
            return self._get_fallback_breakdown(daily_budget, currency)
    
    def _adjust_for_priorities(self, allocation: Dict[str, float], priorities: List[str]) -> Dict[str, float]:
        adjusted = allocation.copy()
        
        priority_weights = {
            "comfort": {"accommodation": 1.3, "misc": 0.7},
            "food_experience": {"food": 1.4, "activities": 0.8},
            "adventure": {"activities": 1.5, "transport": 0.7},
            "budget_saving": {"accommodation": 0.7, "food": 0.7, "activities": 0.6}
        }
        
        for priority in priorities:
            if priority in priority_weights:
                for category, weight in priority_weights[priority].items():
                    if category in adjusted:
                        adjusted[category] = adjusted[category] * weight
        
        total = sum(adjusted.values())
        if total > 0:
            for category in adjusted:
                adjusted[category] = (adjusted[category] / total) * 100
        
        return adjusted
    
    def _assess_deferred_purchase_risks(self, destination: str, risk_tolerance: str) -> List[Dict]:
        deferred_risks = []
        
        common_deferred_items = [
            {"item": "travel_insurance", "risk": "Medical emergency could cost thousands", "advance_savings": "50-100"},
            {"item": "attraction_tickets", "risk": "Sold out or reseller markup", "advance_savings": "20-40%"},
            {"item": "local_sim_card", "risk": "Roaming charges or inability to navigate", "advance_savings": "10-20"},
            {"item": "intercity_transport", "risk": "Last-minute price surge", "advance_savings": "30-50%"}
        ]
        
        for item in common_deferred_items:
            deferred_risks.append({
                "item": item["item"],
                "risk_description": item["risk"],
                "potential_savings_by_prebooking": item["advance_savings"],
                "recommendation": "Book in advance" if risk_tolerance == "low" else "Can defer if flexible"
            })
        
        return deferred_risks
    
    def _generate_group_profile(self, group_size: int, daily_budget: float, breakdown: Dict[str, float]) -> Dict[str, Any]:
        shared_costs = ["accommodation", "transport"]
        individual_costs = ["food", "activities", "misc"]
        
        shared_total = sum(breakdown.get(cat, 0) for cat in shared_costs)
        individual_total = sum(breakdown.get(cat, 0) for cat in individual_costs)
        per_person_shared = shared_total / group_size if group_size > 0 else shared_total
        
        return {
            "group_size": group_size,
            "shared_costs_daily": round(shared_total, 2),
            "per_person_shared_daily": round(per_person_shared, 2),
            "individual_costs_daily": round(individual_total, 2),
            "total_per_person_daily": round(per_person_shared + individual_total, 2),
            "savings_vs_solo": round(individual_total + shared_total - (per_person_shared + individual_total), 2),
            "recommendation": "Split accommodation and transport costs for maximum savings"
        }
    
    def _generate_recommendations(self, quality_risk: Dict, surge_risk: Dict, 
                                  deferred_risks: List, hidden_costs: List) -> List[str]:
        recommendations = []
        
        if quality_risk.get("risk_level") == "high":
            recommendations.append(f"Increase daily budget or choose alternative destination. {quality_risk.get('message', '')}")
        
        if surge_risk.get("risk_level") == "high":
            recommendations.append(f"Book immediately to avoid price surge. {surge_risk.get('expected_increase', '')}")
        
        for risk in deferred_risks:
            if risk.get("recommendation") == "Book in advance":
                recommendations.append(f"Pre-book {risk['item']} to save {risk.get('potential_savings_by_prebooking', 'money')}")
        
        for cost in hidden_costs:
            if cost.get("typical_impact") == "high":
                recommendations.append(cost.get("avoidance_tip", ""))
        
        return recommendations[:5]
    
    def _detect_purchase_category(self, price: float, destination: str) -> str:
        if price < 100:
            return "local_service"
        elif price < 300:
            return "hotel"
        elif price < 1000:
            return "flight"
        else:
            return "package"
    
    def _find_compromise_activities(self, avg_budget: float, currency: str) -> List[str]:
        return [
            "Free walking tours (pay-what-you-want)",
            "Public market visits instead of restaurants",
            "Group cooking class (cost shared)",
            "Half-day free activities + half-day paid",
            "Picnic lunches from local markets"
        ]
    
    def _get_fallback_breakdown(self, daily_budget: float, currency: str) -> Dict[str, float]:
        return {
            "accommodation": round_decimal(daily_budget * 0.40, 2),
            "food": round_decimal(daily_budget * 0.25, 2),
            "activities": round_decimal(daily_budget * 0.20, 2),
            "transport": round_decimal(daily_budget * 0.10, 2),
            "misc": round_decimal(daily_budget * 0.05, 2)
        }