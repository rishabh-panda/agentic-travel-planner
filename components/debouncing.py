"""
Debouncing Component for Agentic Travel Planner
Implements input debouncing to reduce unnecessary processing
"""

import asyncio
from typing import Callable, Any, Optional
from datetime import datetime


class Debouncer:
    """Debounces input events with configurable delay"""
    
    def __init__(self, delay_ms: int = 300):
        self.delay_ms = delay_ms
        self.delay_seconds = delay_ms / 1000
        self.last_call_time = None
        self.pending_call = None
        self.debounce_callbacks = {}
    
    async def debounce(self, callback: Callable, *args, **kwargs) -> Any:
        """Debounce a function call"""
        current_time = datetime.now()
        
        # Cancel pending call if exists
        if self.pending_call:
            self.pending_call.cancel()
        
        # Create new pending call
        self.pending_call = asyncio.create_task(
            self._debounced_call(callback, *args, **kwargs)
        )
        
        return await self.pending_call
    
    async def _debounced_call(self, callback: Callable, *args, **kwargs) -> Any:
        """Internal method to handle debounced call"""
        await asyncio.sleep(self.delay_seconds)
        return callback(*args, **kwargs)
    
    def is_debouncing(self) -> bool:
        """Check if debouncing is in progress"""
        return self.pending_call is not None and not self.pending_call.done()
    
    def reset(self) -> None:
        """Reset debouncer state"""
        if self.pending_call:
            self.pending_call.cancel()
        self.pending_call = None
        self.last_call_time = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "delay_ms": self.delay_ms,
            "delay_seconds": self.delay_seconds,
            "is_debouncing": self.is_debouncing()
        }


class InputDebouncer:
    """Manages debouncing for all input fields"""
    
    def __init__(self, delay_ms: int = 300):
        self.delay_ms = delay_ms
        self.debounce_map = {
            "destination": Debouncer(delay_ms),
            "interests": Debouncer(delay_ms)
        }
    
    async def debounce_destination(self, callback: Callable, *args, **kwargs) -> Any:
        """Debounce destination input"""
        return await self.debounce_map["destination"].debounce(callback, *args, **kwargs)
    
    async def debounce_interests(self, callback: Callable, *args, **kwargs) -> Any:
        """Debounce interests input"""
        return await self.debounce_map["interests"].debounce(callback, *args, **kwargs)
    
    def is_debouncing(self, field: str) -> bool:
        """Check if field is being debounced"""
        if field in self.debounce_map:
            return self.debounce_map[field].is_debouncing()
        return False
    
    def reset(self, field: str = None) -> None:
        """Reset debouncer for specific field or all fields"""
        if field:
            if field in self.debounce_map:
                self.debounce_map[field].reset()
        else:
            for debouncer in self.debounce_map.values():
                debouncer.reset()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "delay_ms": self.delay_ms,
            "debounce_map": {
                field: debouncer.to_dict()
                for field, debouncer in self.debounce_map.items()
            }
        }


# Initialize input debouncer with 300ms delay
input_debouncer = InputDebouncer(delay_ms=300)
