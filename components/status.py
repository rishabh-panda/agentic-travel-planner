"""
Agent Status Update Component for Agentic Travel Planner
Manages status updates for each agent in the generation pipeline
"""

from typing import Dict, Any, Optional
from datetime import datetime


class AgentStatus:
    """Status tracking for individual agents"""
    
    def __init__(self, name: str, progress: int, description: str):
        self.name = name
        self.progress = progress
        self.description = description
        self.start_time = None
        self.end_time = None
        self.status = "pending"  # pending, active, completed, failed
    
    def start(self) -> None:
        """Mark agent as active"""
        self.start_time = datetime.now()
        self.status = "active"
    
    def complete(self) -> None:
        """Mark agent as completed"""
        self.end_time = datetime.now()
        self.status = "completed"
    
    def fail(self, error: str = None) -> None:
        """Mark agent as failed"""
        self.end_time = datetime.now()
        self.status = "failed"
        self.error = error
    
    def get_duration(self) -> float:
        """Get duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "progress": self.progress,
            "description": self.description,
            "status": self.status,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": round(self.get_duration(), 2)
        }


class AgentStatusManager:
    """Manages status updates for all agents in the pipeline"""
    
    def __init__(self):
        self.agents = {}
        self.current_agent = None
        self.total_progress = 0
    
    def add_agent(self, name: str, progress: int, description: str) -> None:
        """Add an agent to the pipeline"""
        self.agents[name] = AgentStatus(name, progress, description)
    
    def start_agent(self, name: str) -> None:
        """Start an agent"""
        if name in self.agents:
            self.agents[name].start()
            self.current_agent = name
            self.total_progress = self.agents[name].progress
    
    def complete_agent(self, name: str) -> None:
        """Complete an agent"""
        if name in self.agents:
            self.agents[name].complete()
            self.total_progress = self.agents[name].progress
    
    def fail_agent(self, name: str, error: str = None) -> None:
        """Mark an agent as failed"""
        if name in self.agents:
            self.agents[name].fail(error)
            self.total_progress = self.agents[name].progress
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of all agents"""
        return {
            "total_progress": self.total_progress,
            "current_agent": self.current_agent,
            "agents": {name: agent.to_dict() for name, agent in self.agents.items()}
        }
    
    def reset(self) -> None:
        """Reset all agent statuses"""
        self.agents = {}
        self.current_agent = None
        self.total_progress = 0
        
        # Re-initialize agents
        self.add_agent("Research Agent", 25, "Finding attractions and weather information...")
        self.add_agent("Budget Agent", 50, "Calculating budget breakdown...")
        self.add_agent("Logistics Agent", 75, "Creating day-by-day itinerary...")
        self.add_agent("Summariser Agent", 90, "Generating final itinerary summary...")
        self.add_agent("Complete", 100, "Generation complete!")


# Initialize default agent pipeline
status_manager = AgentStatusManager()
status_manager.add_agent("Research Agent", 25, "Finding attractions and weather information...")
status_manager.add_agent("Budget Agent", 50, "Calculating budget breakdown...")
status_manager.add_agent("Logistics Agent", 75, "Creating day-by-day itinerary...")
status_manager.add_agent("Summariser Agent", 90, "Generating final itinerary summary...")
status_manager.add_agent("Complete", 100, "Generation complete!")
