"""
Constants for cost calculations across the budget system.
"""

HIDDEN_COST_CATEGORIES = {
    "resort_fees": {
        "description": "Mandatory daily fees for amenities you may not use",
        "base_cost": 25.00,
        "applicable_to": ["mid-range", "luxury"],
        "avoidance_tip": "Filter hotels by 'all-inclusive pricing' or call to confirm total nightly cost",
        "typical_impact": "high"
    },
    "baggage_fees": {
        "description": "Airline fees for checked or carry-on luggage",
        "base_cost": 35.00,
        "applicable_to": ["budget", "mid-range"],
        "avoidance_tip": "Fly with airlines that include baggage or pack light",
        "typical_impact": "medium"
    },
    "airport_transport": {
        "description": "Cost to get from airport to city center",
        "base_cost": 20.00,
        "applicable_to": ["all"],
        "avoidance_tip": "Research public transport options before arriving",
        "typical_impact": "medium"
    },
    "dynamic_currency_conversion": {
        "description": "Extra fees when paying in your home currency abroad",
        "base_cost": 5.00,
        "applicable_to": ["all"],
        "avoidance_tip": "Always pay in local currency when using cards",
        "typical_impact": "low"
    },
    "service_charges": {
        "description": "Mandatory tips or service fees not included in listed prices",
        "base_cost": 10.00,
        "applicable_to": ["mid-range", "luxury"],
        "avoidance_tip": "Check if service charge is already included before adding extra tip",
        "typical_impact": "low"
    }
}

QUALITY_THRESHOLDS = {
    "budget": {
        "min_daily_usd": 30,
        "max_daily_usd": 70,
        "warning_threshold": 25
    },
    "mid-range": {
        "min_daily_usd": 70,
        "max_daily_usd": 150,
        "warning_threshold": 50
    },
    "luxury": {
        "min_daily_usd": 150,
        "max_daily_usd": 500,
        "warning_threshold": 100
    }
}

RISK_FACTORS = {
    "travel_insurance": {
        "last_minute_threshold": 3,
        "last_minute_multiplier": 2.0,
        "medium_window": 14,
        "medium_multiplier": 1.3,
        "risks": ["Medical emergency", "Trip cancellation", "Lost baggage"]
    },
    "attraction_tickets": {
        "last_minute_threshold": 7,
        "last_minute_multiplier": 1.5,
        "medium_window": 30,
        "medium_multiplier": 1.2,
        "risks": ["Sold out", "Long queues", "Reseller markup"]
    },
    "accommodation": {
        "last_minute_threshold": 14,
        "last_minute_multiplier": 1.4,
        "medium_window": 60,
        "medium_multiplier": 1.1,
        "risks": ["Limited options", "Price surge", "Poor locations"]
    },
    "flights": {
        "last_minute_threshold": 21,
        "last_minute_multiplier": 1.6,
        "medium_window": 90,
        "medium_multiplier": 1.15,
        "risks": ["Full flights", "Premium pricing", "Bad connections"]
    }
}

DEFAULT_ALLOCATION_PERCENTAGES = {
    "budget": {
        "accommodation": 35,
        "food": 20,
        "activities": 15,
        "transport": 20,
        "misc": 10
    },
    "mid-range": {
        "accommodation": 40,
        "food": 25,
        "activities": 20,
        "transport": 10,
        "misc": 5
    },
    "luxury": {
        "accommodation": 45,
        "food": 25,
        "activities": 20,
        "transport": 5,
        "misc": 5
    }
}

DESTINATION_COST_MULTIPLIERS = {
    "Western Europe": 1.3,
    "North America": 1.3,
    "Australia": 1.2,
    "Japan": 1.1,
    "Eastern Europe": 0.8,
    "Southeast Asia": 0.5,
    "South Asia": 0.4,
    "South America": 0.7,
    "Africa": 0.6,
    "Middle East": 0.9
}