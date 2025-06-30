from typing import Dict, List, Optional
import numpy as np
from datetime import datetime, timedelta

from ..interfaces.base import Device, Agent
from ..utils.config import config

class SimulationEnvironment:
    """Environment for simulating home automation scenarios."""
    
    def __init__(self):
        """Initialize simulation environment."""
        self.timestep = config.get("simulation.timestep", 300)  # 5 minutes default
        self.duration = config.get("simulation.duration", 86400)  # 24 hours default
        self.current_time = 0
        self.devices: Dict[str, Device] = {}
        self.agents: List[Agent] = []
        self.state_history: List[Dict] = []
    
    def add_device(self, name: str, device: Device) -> None:
        """Add a device to the environment."""
        self.devices[name] = device
    
    def add_agent(self, agent: Agent) -> None:
        """Add an agent to the environment."""
        self.agents.append(agent)
    
    def get_state(self) -> Dict:
        """Get current environment state."""
        return {
            "timestamp": self.current_time,
            "devices": {name: device.read() for name, device in self.devices.items()}
        }
    
    def step(self) -> Dict:
        """Advance simulation by one timestep."""
        # Get current state
        state = self.get_state()
        
        # Let agents observe and act
        for agent in self.agents:
            agent.observe(state)
            action = agent.decide()
            agent.act(action)
        
        # Record state
        self.state_history.append(state)
        
        # Advance time
        self.current_time += self.timestep
        
        return state
    
    def run(self) -> List[Dict]:
        """Run full simulation."""
        while self.current_time < self.duration:
            self.step()
        return self.state_history
    
    def reset(self) -> None:
        """Reset simulation state."""
        self.current_time = 0
        self.state_history.clear()
