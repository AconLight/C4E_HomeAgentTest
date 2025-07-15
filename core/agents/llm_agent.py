from typing import Any, Dict, List, Optional
import numpy as np

from ..interfaces.base import Agent
from ..utils.config import config

class LLMAgent(Agent):
    """Simple rule-based agent for testing."""
    
    def __init__(self):
        """Initialize the agent."""
        return
    
    def ask(self, prompt: str) -> str:
        """Placeholder for LLM Q&A method."""
        return ""
