# Agentic Travel Itinerary Planner

Multi-agent travel planning system using Groq's free LLM API. Research attractions, calculate budgets, and generate personalized day-by-day itineraries.

## Features

- Research Agent: Searches attractions and fetches weather forecasts
- Budget Agent: Calculates daily expense breakdowns
- Logistics Agent: Creates day-by-day itineraries
- Summariser Agent: Produces polished travel plans
- Supports multiple currencies including INR

## Tech Stack

- LangGraph for agent orchestration
- Groq (Llama 3.3 70B) for LLM
- Streamlit for UI
- DuckDuckGo search, Open-Meteo weather, Frankfurter exchange rates

## Installation

```bash
git clone <repository-url>
cd agentic-travel-planner
py -3.10 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration
Create .env file:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

## Usage
```bash
streamlit run app.py
```