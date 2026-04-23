from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


class BudgetBreakdown(BaseModel):
    accommodation: float
    food: float
    activities: float
    transport: float
    misc: float
    
    class Config:
        json_schema_extra = {
            "example": {
                "accommodation": 80.00,
                "food": 50.00,
                "activities": 40.00,
                "transport": 20.00,
                "misc": 10.00
            }
        }


class HiddenCostWarning(BaseModel):
    category: str
    description: str
    estimated_cost: float
    avoidance_tip: str
    typical_impact: str


class GroupBudgetProfile(BaseModel):
    group_size: int
    shared_costs_daily: float
    per_person_shared_daily: float
    individual_costs_daily: float
    total_per_person_daily: float
    savings_vs_solo: float
    recommendation: str


class RiskAssessment(BaseModel):
    item_type: str
    current_price: float
    estimated_deferred_price: float
    additional_cost_if_deferred: float
    urgency_level: str
    recommendation: str
    risk_factors: List[str] = []


class QualityRisk(BaseModel):
    risk_level: str
    message: str
    suggested_action: str


class BudgetRequest(BaseModel):
    total_budget: float = Field(gt=0, description="Total budget amount")
    currency: str = Field(min_length=3, max_length=3, description="Currency code")
    days: int = Field(gt=0, le=365, description="Number of days")
    destination: str = Field(min_length=1, description="Travel destination")
    traveller_type: str = Field(default="mid-range", pattern="^(budget|mid-range|luxury)$")
    group_size: int = Field(default=1, ge=1, le=50)
    booking_window_days: int = Field(default=60, ge=0, le=365)
    include_hidden_costs: bool = Field(default=True)
    risk_tolerance: str = Field(default="medium", pattern="^(low|medium|high)$")
    travel_style_priorities: List[str] = Field(default=[])
    
    @validator('currency')
    def currency_uppercase(cls, v):
        return v.upper()


class BudgetResponse(BaseModel):
    total_budget: float
    original_currency: str
    base_currency: str
    days: int
    daily_budget: float
    true_daily_cost: float
    destination: str
    traveller_type: str
    breakdown: Dict[str, float]
    hidden_costs: List[Dict[str, Any]]
    quality_warning: Dict[str, Any]
    surge_risk: Dict[str, Any]
    deferred_purchase_risks: List[Dict[str, Any]]
    group_profile: Optional[Dict[str, Any]]
    recommendations: List[str]
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }