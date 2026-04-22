import os
import streamlit as st
from dotenv import load_dotenv
from agents.orchestrator import Orchestrator

load_dotenv()


def validate_environment() -> bool:
    """Validate required environment variables."""
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key or not api_key.strip():
        st.error("GROQ_API_KEY not found in .env file")
        st.info("Get your free key at: https://console.groq.com")
        return False
    
    return True


def create_travel_plan(destination, days, budget, currency, interests):
    """Create travel plan using agent orchestrator."""
    
    if not destination or not destination.strip():
        return "ERROR: Please enter a destination."
    
    if days < 1 or days > 14:
        return "ERROR: Days must be between 1 and 14."
    
    if budget < 50:
        return "ERROR: Budget must be at least 50 USD (or equivalent)."
    
    if not interests or not interests.strip():
        return "ERROR: Please enter at least one interest."
    
    try:
        orchestrator = Orchestrator()
        
        result = orchestrator.create_travel_plan(
            destination=destination.strip(),
            days=int(days),
            budget=float(budget),
            currency=currency.strip().upper(),
            interests=interests.strip()
        )
        
        if result.get("success"):
            return result.get("final_itinerary", "No itinerary generated.")
        else:
            return f"ERROR: {result.get('error', 'Unknown error occurred')}"
    
    except Exception as e:
        return f"ERROR: Unexpected error - {str(e)}"


def main():
    st.set_page_config(
        page_title="Agentic Travel Itinerary Planner",
        page_icon="✈️",
        layout="wide"
    )
    
    st.title("Agentic Travel Itinerary Planner")
    st.markdown("""
    This application uses multiple AI agents to create a personalized travel itinerary.
    
    **How it works:**
    1. Research Agent finds attractions and weather
    2. Budget Agent calculates daily expenses  
    3. Logistics Agent creates day-by-day plan
    4. Summariser Agent produces final itinerary
    
    All agents run on Groq's free tier (Llama 3.3 70B).
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        destination = st.text_input(
            "Destination",
            placeholder="e.g., Paris, Tokyo, New York, Gurugram"
        )
        
        days = st.slider(
            "Number of Days",
            min_value=1,
            max_value=14,
            value=3
        )
        
        budget = st.number_input(
            "Total Budget",
            min_value=50.0,
            value=1000.0,
            step=50.0
        )
        
        currency = st.selectbox(
            "Currency",
            options=["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "INR", "CNY", "SGD"],
            index=0
        )
        
        interests = st.text_area(
            "Interests (comma-separated)",
            placeholder="e.g., history, food, museums, hiking, shopping, clubbing",
            height=100
        )
        
        generate_button = st.button("Generate Travel Plan", type="primary")
    
    with col2:
        output_placeholder = st.empty()
    
    if generate_button:
        with st.spinner("Creating your personalized itinerary... This may take 15-30 seconds."):
            result = create_travel_plan(destination, days, budget, currency, interests)
            output_placeholder.text_area(
                "Your Personalized Itinerary",
                value=result,
                height=600,
                key="itinerary_output"
            )
    
    st.markdown("---")
    st.markdown("""
    **Tips:**
    - Be specific about your interests for better recommendations
    - Budget should be realistic for your destination
    - The plan uses free APIs - some data may be approximate
    - Generation takes 15-30 seconds due to multiple agent calls
    """)


if __name__ == "__main__":
    if validate_environment():
        main()