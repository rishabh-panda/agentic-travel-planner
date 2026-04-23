"""
Agentic Travel Itinerary Planner
Enterprise-Grade User Interface
Version: 2.0.1
"""

import os
import sys
from pathlib import Path

# Explicitly load environment variables from .env file BEFORE any other imports
from dotenv import load_dotenv

# Get the absolute path to the .env file (project root)
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Debug: Verify API key is loaded (remove in production)
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("WARNING: GROQ_API_KEY environment variable is not set.")
    print(f"Looking for .env file at: {env_path}")
    if env_path.exists():
        print(".env file found but GROQ_API_KEY is missing or empty.")
    else:
        print(f".env file not found at {env_path}")

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from typing import Dict, Any, Optional
import traceback

# Import agents after environment is configured
from agents.orchestrator import Orchestrator

# Import UI components
from components.export import export_to_txt, export_to_markdown, export_to_pdf
from components.export import create_export_filename, is_pdf_available
from components.sharing import copy_to_clipboard, create_email_share_link
from components.sharing import generate_shareable_link, show_share_options
from utils.caching import load_from_cache, save_to_cache, generate_cache_key
from components.export_buttons import create_export_section, is_export_enabled

# Import error handling components
from components.api_key_error import APIKeyErrorBanner
from components.generation_error import GenerationErrorBox
from components.budget_recommendations import BudgetRecommendations
from components.weather_fallback import WeatherFallback
from components.session_handling import SessionHandler

# Page configuration
st.set_page_config(
    page_title="Agentic Travel Itinerary Planner",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def load_custom_css() -> str:
    """Returns custom CSS for professional UI styling."""
    return """
    <style>
        /* Import external CSS files */
        @import url('styles/theme.css');
        @import url('styles/responsive.css');
        @import url('styles/accessibility.css');
        
        /* Main container styling */
        .main {
            padding: 0rem 1rem;
        }
        
        /* Skip Links */
        .skip-links {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 1000;
        }
        
        .skip-link {
            position: absolute;
            top: -40px;
            left: 50%;
            transform: translateX(-50%);
            background: #1E3A5F;
            color: white;
            padding: 0.5rem 1rem;
            z-index: 100;
            text-decoration: none;
            font-weight: 600;
            border-radius: 8px;
            transition: top 0.2s ease;
        }
        
        .skip-link:focus {
            top: 0;
            outline: 2px solid #1E3A5F;
            outline-offset: 2px;
        }
        
        /* Screen Reader Only Text */
        .sr-only {
            position: absolute;
            width: 1px;
            height: 1px;
            padding: 0;
            margin: -1px;
            overflow: hidden;
            clip: rect(0, 0, 0, 0);
            white-space: nowrap;
            border: 0;
        }
        
        /* Focus Indicators */
        :focus {
            outline: 2px solid #1E3A5F;
            outline-offset: 2px;
        }
        
        :focus-visible {
            outline: 2px solid #1E3A5F;
            outline-offset: 2px;
        }
        
        /* Card styling */
        .stCard {
            background-color: #FFFFFF;
            border-radius: 12px;
            border: 1px solid #E5E7EB;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
        }
        
        .stCard:hover {
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Header styling */
        .main-header {
            background: linear-gradient(135deg, #1E3A5F 0%, #2C4A6E 100%);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            color: white;
        }
        
        .main-header h1 {
            margin: 0;
            font-size: 2rem;
            font-weight: 600;
        }
        
        .main-header p {
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
        }
        
        /* Button styling */
        .stButton button {
            background: linear-gradient(135deg, #1E3A5F 0%, #008080 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.5rem;
            font-weight: 500;
            transition: all 0.2s ease;
            width: 100%;
        }
        
        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(30,58,95,0.2);
        }
        
        .stButton button:disabled {
            opacity: 0.6;
            transform: none;
        }
        
        /* Input field styling */
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            border-radius: 8px;
            border: 1px solid #D1D5DB;
            transition: all 0.2s ease;
        }
        
        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
            outline: 2px solid #1E3A5F;
            outline-offset: 2px;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background-color: #F3F4F6;
            border-radius: 8px;
            padding: 0.25rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 6px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            color: #6B7280;
            transition: all 0.2s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF;
            color: #1E3A5F;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        
        /* Metric card styling */
        .metric-card {
            background-color: #F8F9FA;
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
            border: 1px solid #E5E7EB;
            transition: all 0.2s ease;
        }
        
        .metric-card:hover {
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .metric-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: #1E3A5F;
        }
        
        .metric-label {
            font-size: 0.875rem;
            color: #6B7280;
            margin-top: 0.25rem;
        }
        
        /* Info box styling */
        .info-box {
            background-color: #F0F9FF;
            border-left: 4px solid #008080;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .warning-box {
            background-color: #FEF3C7;
            border-left: 4px solid #F59E0B;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .error-box {
            background-color: #FEE2E2;
            border-left: 4px solid #DC2626;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        /* Divider */
        .custom-divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, #D1D5DB, transparent);
            margin: 1.5rem 0;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 2rem;
            color: #9CA3AF;
            font-size: 0.75rem;
            border-top: 1px solid #E5E7EB;
            margin-top: 2rem;
        }
        
        /* Loading spinner */
        .stSpinner > div {
            border-color: #1E3A5F transparent transparent transparent;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main-header {
                padding: 1rem;
            }
            .main-header h1 {
                font-size: 1.5rem;
            }
            .metric-value {
                font-size: 1.25rem;
            }
        }
        
        /* High Contrast Mode Support */
        @media (prefers-contrast: more) {
            :focus,
            :focus-visible {
                outline: 3px solid #000000;
                outline-offset: 2px;
            }
            
            .stCard,
            .metric-card {
                border: 1px solid #000000;
            }
        }
        
        /* Reduced Motion Support */
        @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
    """


def create_budget_chart(breakdown: Dict[str, float], currency: str) -> go.Figure:
    """Creates a professional budget breakdown chart using Plotly."""
    try:
        if not breakdown:
            return go.Figure()
        
        categories = list(breakdown.keys())
        amounts = list(breakdown.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=amounts,
                marker_color=['#1E3A5F', '#008080', '#2C4A6E', '#3B6B8F', '#4A8DAF'],
                text=[f"{currency} {amt:.0f}" for amt in amounts],
                textposition='outside',
                name='Daily Budget'
            )
        ])
        
        fig.update_layout(
            title="Budget Breakdown by Category",
            xaxis_title="Category",
            yaxis_title=f"Amount ({currency})",
            template="plotly_white",
            height=400,
            margin=dict(l=40, r=40, t=60, b=40),
            font=dict(family="Inter, sans-serif", size=12)
        )
        
        fig.update_traces(
            hovertemplate=f"<b>%{{x}}</b><br>Amount: %{{y:,.2f}} {currency}<extra></extra>"
        )
        
        return fig
    except Exception as e:
        print(f"Chart creation error: {e}")
        return go.Figure()


def create_weather_table(forecast: list) -> pd.DataFrame:
    """Creates a formatted weather DataFrame."""
    try:
        if not forecast:
            return pd.DataFrame()
        
        weather_data = []
        for day in forecast[:5]:
            weather_data.append({
                "Date": day.get("date", "Unknown"),
                "Condition": day.get("condition", "Unknown"),
                "Temperature": f"{day.get('temp', 'N/A')}°C"
            })
        return pd.DataFrame(weather_data)
    except Exception as e:
        print(f"Weather table error: {e}")
        return pd.DataFrame()


def render_sidebar_info() -> None:
    """Renders the sidebar with helpful information."""
    with st.sidebar:
        st.markdown("### About")
        st.markdown("This tool uses multiple AI agents to create personalized travel itineraries.")
        
        st.markdown("### How It Works")
        st.markdown("""
        1. Research Agent finds attractions and weather
        2. Budget Agent calculates daily expenses
        3. Logistics Agent creates day-by-day plan
        4. Summariser Agent produces final itinerary
        """)
        
        st.markdown("### Tips")
        st.markdown("""
        - Be specific about your interests
        - Budget should be realistic for destination
        - Generation takes 15-30 seconds
        """)
        
        st.markdown("### Supported Currencies")
        st.markdown("INR, USD, EUR, GBP, JPY, CAD, AUD, SGD, CNY")


def initialize_session_state() -> None:
    """Initializes session state variables."""
    defaults = {
        "generated": False,
        "itinerary": None,
        "error": None,
        "loading": False,
        "research": None,
        "budget": None,
        "logistics": None,
        "api_key_error": None,
        "generation_error": None,
        "session_handler": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def initialize_error_handlers() -> None:
    """Initialize error handling components."""
    if st.session_state.get("api_key_error") is None:
        st.session_state.api_key_error = APIKeyErrorBanner()
    
    if st.session_state.get("generation_error") is None:
        st.session_state.generation_error = GenerationErrorBox()
    
    if st.session_state.get("budget_recommendations") is None:
        st.session_state.budget_recommendations = BudgetRecommendations()
    
    if st.session_state.get("weather_fallback") is None:
        st.session_state.weather_fallback = WeatherFallback()
    
    if st.session_state.get("session_handler") is None:
        st.session_state.session_handler = SessionHandler()


def check_api_key_status() -> bool:
    """Validates that GROQ_API_KEY is properly configured."""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.sidebar.error(
            "GROQ_API_KEY not found. Please ensure your .env file contains GROQ_API_KEY=your_key_here"
        )
        return False
    
    if api_key == "your_groq_api_key_here":
        st.sidebar.warning(
            "GROQ_API_KEY is using the default placeholder. Please update your .env file with a valid API key."
        )
        return False
    
    return True


def main() -> None:
    """Main application entry point."""
    
    # Load custom CSS
    st.markdown(load_custom_css(), unsafe_allow_html=True)
    
    # Skip Links
    st.markdown("""
    <div class="skip-links">
        <a href="#main-content" class="skip-link">Skip to main content</a>
        <a href="#navigation" class="skip-link">Skip to navigation</a>
        <a href="#results" class="skip-link">Skip to results</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize error handlers
    initialize_error_handlers()
    
    # Render sidebar
    render_sidebar_info()
    
    # Check API key status
    api_valid = check_api_key_status()
    
    # Display API key error banner if needed
    api_key_error = st.session_state.api_key_error
    if api_key_error:
        error_info = api_key_error.check_api_key_status()
        if error_info.get("has_error"):
            st.markdown(api_key_error.get_error_html(error_info), unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <header class="main-header" role="banner">
        <h1>Agentic Travel Itinerary Planner</h1>
        <p>AI-powered personalized travel planning using Groq Llama 3.3 70B</p>
    </header>
    """, unsafe_allow_html=True)
    
    # Two-column layout for input
    col_left, col_right = st.columns([0.4, 0.6])
    
    with col_left:
        st.markdown("### Trip Details")
        
        with st.container():
            destination = st.text_input(
                "Destination",
                placeholder="e.g., Delhi, Copenhagen, Tokyo",
                help="Enter any city or region worldwide",
                key="destination_input"
            )
            
            col_days, col_budget = st.columns(2)
            with col_days:
                days = st.number_input(
                    "Number of Days",
                    min_value=1,
                    max_value=14,
                    value=3,
                    step=1,
                    help="Trip duration in days (1-14)",
                    key="days_input"
                )
            with col_budget:
                budget = st.number_input(
                    "Total Budget",
                    min_value=1.0,
                    value=35000.0,
                    step=1000.0,
                    help="Your total trip budget",
                    key="budget_input"
                )
            
            currency = st.selectbox(
                "Currency",
                options=["INR", "USD", "EUR", "GBP", "JPY", "CAD", "AUD", "SGD"],
                index=0,
                help="Select your preferred currency",
                key="currency_select"
            )
            
            interests = st.text_area(
                "Interests",
                placeholder="e.g., Culture, Food, Adventure, History, Shopping",
                help="Comma-separated list of your interests",
                height=100,
                key="interests_input"
            )
            
            st.markdown("")
            
            # Export button state management
            export_enabled = is_export_enabled(
                st.session_state.itinerary if hasattr(st.session_state, 'itinerary') else None,
                destination
            )
            
            # Display export button state
            if not export_enabled and destination:
                st.markdown("""
                <div class="info-box" role="status" aria-live="polite">
                    <strong>Export Available:</strong> Generate a travel plan to enable export functionality
                </div>
                """, unsafe_allow_html=True)
            
            # Generate button with loading state
            generate_disabled = st.session_state.loading or not api_valid or not destination
            generate_button = st.button(
                "Generate Travel Plan",
                type="primary",
                width='stretch',
                disabled=generate_disabled,
                key="generate_button"
            )
    
    with col_right:
        st.markdown("### Destination Preview")
        
        # Placeholder for destination preview
        if destination:
            st.markdown(f"""
            <div class="metric-card" role="region" aria-label="Destination preview card">
                <div class="metric-value">{destination}</div>
                <div class="metric-label">{days} day{'s' if days > 1 else ''} trip</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick budget indicator
            if budget > 0:
                daily_budget = budget / days
                if currency == "INR":
                    is_low = daily_budget < 3000
                    is_high = daily_budget > 15000
                elif currency == "USD":
                    is_low = daily_budget < 50
                    is_high = daily_budget > 250
                else:
                    is_low = False
                    is_high = False
                
                if is_low:
                    st.markdown("""
                    <div class="warning-box" role="alert" aria-live="polite">
                        <strong>Budget Advisory:</strong> Your daily budget appears low for this destination. Consider increasing or choosing a more affordable destination.
                    </div>
                    """, unsafe_allow_html=True)
                elif is_high:
                    st.markdown("""
                    <div class="info-box" role="status" aria-live="polite">
                        <strong>Budget is Healthy:</strong> Your budget should provide a comfortable experience.
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box" role="status" aria-live="polite">
                Enter a destination to see preview information.
            </div>
            """, unsafe_allow_html=True)
    
    # Generation logic
    if generate_button:
        if not destination:
            st.error("Please enter a destination.")
            return
        
        # Check for cached results first
        cache_key = generate_cache_key(destination, days, budget, currency, interests)
        cached_results = load_from_cache(destination, days, budget, currency, interests)
        
        if cached_results and cached_results.get("success"):
            # Use cached results
            st.session_state.itinerary = cached_results.get("final_itinerary", "")
            st.session_state.research = cached_results.get("research", {})
            st.session_state.budget = cached_results.get("budget", {})
            st.session_state.logistics = cached_results.get("logistics", {})
            st.session_state.generated = True
            st.session_state.error = None
            st.info("Loaded results from cache (24-hour cache)")
            
            # Auto scroll to results using JavaScript
            st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
        else:
            # Generate new results
            st.session_state.loading = True
            st.session_state.generated = False
            st.session_state.error = None
        
        try:
            with st.spinner("Planning your trip... This may take 15-30 seconds."):
                orchestrator = Orchestrator()
                result = orchestrator.create_travel_plan(
                    destination=destination,
                    days=days,
                    budget=budget,
                    currency=currency,
                    interests=interests
                )
            
            if result.get("success"):
                st.session_state.itinerary = result.get("final_itinerary", "")
                st.session_state.research = result.get("research", {})
                st.session_state.budget = result.get("budget", {})
                st.session_state.logistics = result.get("logistics", {})
                st.session_state.generated = True
                st.session_state.error = None
                
                # Cache results for 24 hours
                cache_key = generate_cache_key(destination, days, budget, currency, interests)
                save_to_cache(
                    destination=destination,
                    days=days,
                    budget=budget,
                    currency=currency,
                    interests=interests,
                    results=result
                )
                
                # Auto scroll to results using JavaScript
                st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
            else:
                st.session_state.error = result.get("error", "Unknown error occurred")
                st.session_state.generated = False
                
        except Exception as e:
            error_msg = str(e)
            st.session_state.error = error_msg
            st.session_state.generated = False
            print(f"Generation error details: {traceback.format_exc()}")
        finally:
            st.session_state.loading = False
    
    # Display results
    if st.session_state.generated and st.session_state.itinerary:
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("### Your Personalized Itinerary")
        
        # Tabbed interface for results
        tab1, tab2, tab3, tab4 = st.tabs([
            "Daily Itinerary", "Budget Analysis", "Weather Forecast", "Travel Tips"
        ])
        
        with tab1:
            st.markdown(st.session_state.itinerary)
            
            # Export options using new component
            st.markdown("")
            create_export_section(
                st.session_state.itinerary,
                destination,
                days,
                budget,
                currency,
                st.session_state.budget,
                st.session_state.research.get("weather", {})
            )
        
        with tab2:
            budget_info = st.session_state.budget
            if budget_info:
                breakdown = budget_info.get("breakdown", {})
                currency_code = budget_info.get("currency", "INR")
                
                # Summary metrics
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                with col_m1:
                    st.markdown(f"""
                    <div class="metric-card" role="region" aria-label="Total budget metric">
                        <div class="metric-value">{currency_code} {budget_info.get('total_budget', 0):,.0f}</div>
                        <div class="metric-label">Total Budget</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_m2:
                    st.markdown(f"""
                    <div class="metric-card" role="region" aria-label="Daily budget metric">
                        <div class="metric-value">{currency_code} {budget_info.get('daily_budget', 0):,.0f}</div>
                        <div class="metric-label">Daily Budget</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_m3:
                    st.markdown(f"""
                    <div class="metric-card" role="region" aria-label="Number of days metric">
                        <div class="metric-value">{budget_info.get('days', 0)}</div>
                        <div class="metric-label">Days</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_m4:
                    risk = budget_info.get("quality_warning", {}).get("risk_level", "Unknown")
                    risk_color = "#10B981" if risk == "low" else "#F59E0B" if risk == "medium" else "#EF4444"
                    st.markdown(f"""
                    <div class="metric-card" role="region" aria-label="Budget risk level metric">
                        <div class="metric-value" style="color: {risk_color};">{risk.upper()}</div>
                        <div class="metric-label">Budget Risk Level</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("")
                
                if breakdown:
                    fig = create_budget_chart(breakdown, currency_code)
                    st.plotly_chart(fig, width='stretch')
                
                # Detailed breakdown table
                st.markdown("#### Detailed Breakdown")
                breakdown_data = []
                daily_budget_val = budget_info.get('daily_budget', 1)
                for cat, amt in breakdown.items():
                    pct = (amt / daily_budget_val * 100) if daily_budget_val > 0 else 0
                    breakdown_data.append({
                        "Category": cat.capitalize(),
                        "Daily Amount": f"{currency_code} {amt:.2f}",
                        "Percentage": f"{pct:.0f}%"
                    })
                st.dataframe(pd.DataFrame(breakdown_data), width='stretch', hide_index=True)
                
                # Quality warning
                quality = budget_info.get("quality_warning", {})
                if quality.get("message"):
                    msg_type = "warning-box" if quality.get("risk_level") in ["high", "critical"] else "info-box"
                    st.markdown(f"""
                    <div class="{msg_type}" role="alert" aria-live="polite">
                        <strong>Budget Assessment:</strong> {quality.get('message')}<br>
                        <strong>Recommendation:</strong> {quality.get('suggested_action', '')}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Budget recommendations
                budget_recommendations = st.session_state.budget_recommendations
                if budget_recommendations:
                    daily_budget = budget_info.get('daily_budget', budget)
                    recommendations = budget_recommendations.get_recommendations(
                        daily_budget=daily_budget,
                        currency=currency_code,
                        days=budget_info.get('days', days)
                    )
                    
                    if recommendations.get("has_recommendations"):
                        # Display critical alert if needed
                        alert = recommendations.get("alert")
                        if alert and alert.get("should_animate"):
                            st.markdown(budget_recommendations.get_critical_alert_html(alert), unsafe_allow_html=True)
                        elif alert:
                            st.markdown(budget_recommendations.get_warning_alert_html(alert), unsafe_allow_html=True)
                        
                        # Display recommendations
                        st.markdown(budget_recommendations.get_recommendations_html(recommendations.get("recommendations", [])), unsafe_allow_html=True)
        
        with tab3:
            weather_info = st.session_state.research.get("weather", {})
            forecast = weather_info.get("forecast", [])
            if forecast:
                weather_df = create_weather_table(forecast)
                st.dataframe(weather_df, width='stretch', hide_index=True)
            else:
                # Use weather fallback component
                weather_fallback = st.session_state.weather_fallback
                if weather_fallback:
                    estimated_weather = weather_fallback.estimate_weather(
                        destination=destination,
                        season="spring",
                        days=days
                    )
                    st.markdown(weather_fallback.get_fallback_html(estimated_weather), unsafe_allow_html=True)
                else:
                    st.info("Weather data not available for this destination.")
        
        with tab4:
            st.markdown("#### Recommended Tips")
            
            # Hidden costs tips
            hidden_costs = st.session_state.budget.get("hidden_costs", [])
            if hidden_costs:
                st.markdown("**Hidden Costs to Avoid:**")
                for hc in hidden_costs[:3]:
                    st.markdown(f"- **{hc.get('category', 'Unknown')}:** {hc.get('avoidance_tip', 'No tip available')}")
            
            # Recommendations
            recommendations = st.session_state.budget.get("recommendations", [])
            if recommendations:
                st.markdown("**Recommendations:**")
                for rec in recommendations[:3]:
                    st.markdown(f"- {rec}")
            
            # General tips
            st.markdown("**General Travel Tips:**")
            st.markdown("""
            - Book accommodations in advance for better rates
            - Consider travel insurance for expensive trips
            - Download offline maps before arrival
            - Learn a few local phrases
            - Keep digital and physical copies of important documents
            """)
    
    elif st.session_state.error:
        # Use generation error component for better error display
        generation_error = st.session_state.generation_error
        if generation_error:
            error_info = generation_error.create_error_box(
                error_message=st.session_state.error,
                error_type="unknown_error"
            )
            st.markdown(generation_error.get_error_html(error_info), unsafe_allow_html=True)
        else:
            # Fallback to basic error display
            st.markdown(f"""
            <div class="error-box" role="alert" aria-live="assertive">
                <strong>Error:</strong> {st.session_state.error}<br><br>
                Please check your inputs and try again. If the problem persists, verify your API keys and internet connection.
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <footer class="footer" role="contentinfo">
        Powered by Groq Llama 3.3 70B | Weather: Open-Meteo | Currency: Frankfurter API
    </footer>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()