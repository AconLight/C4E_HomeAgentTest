from typing import Any, Dict, List, Optional
import numpy as np

from ..interfaces.base import Agent
from ..utils.config import config

class LLMAgent(Agent):
    """Simple rule-based agent for testing."""
    
    def __init__(self):
        """Initialize the agent."""
        self.state_history: List[Dict[str, Any]] = []
    
    def observe(self, state: Dict[str, Any]) -> None:
        """Process new observation."""
        self.state_history.append(state)
        if len(self.state_history) > 100:  # Keep last 100 states
            self.state_history.pop(0)
    
    def decide(self) -> Dict[str, Any]:
        """Make a decision based on current state."""
        if not self.state_history:
            return {"action": "no_op"}
            
        current_state = self.state_history[-1]
        sensors = current_state.get("sensors", {})
        
        # Simple rule-based decision making
        if "temperature" in sensors:
            temp = sensors["temperature"]
            if temp > 24:
                return {"action": "cool_down"}
            elif temp < 20:
                return {"action": "heat_up"}
                
        return {"action": "maintain"}
        
        decision_text = self.tokenizer.decode(outputs[0])
        return self._parse_decision(decision_text)
    
    def act(self, action: Dict[str, Any]) -> bool:
        """Execute an action."""
        # For testing purposes, always return success
        return True
    
    def _prepare_context(self) -> str:
        """Prepare context string from state history."""
        context = "Current environment state:\n"
        for state in self.state_history[-5:]:  # Last 5 states
            context += f"Time: {state['timestamp']}\n"
            for sensor, value in state['sensors'].items():
                context += f"{sensor}: {value}\n"
        return context
    
    def _parse_decision(self, text: str) -> Dict[str, Any]:
        """Parse model output into structured decision."""
        # Implement decision parsing logic here
        # This is a placeholder implementation
        return {"action": "no_op"}
    
    def ask(self, prompt: str) -> str:
        """Placeholder for LLM Q&A method."""
        return ""
