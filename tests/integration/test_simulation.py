import pytest
from pathlib import Path
import sys
from typing import Dict, List, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from core.simulation.environment import SimulationEnvironment
from core.agents.llm_agent import LLMAgent
from core.strategy.energy_optimization import EnergyOptimizationStrategy
from core.interfaces.base import Device

class TestDevice(Device):
    def __init__(self, initial_value=20.0, step_delta=0.1):
        self.value = initial_value
        self.step_delta = step_delta
        self.value_type = "measurement"
    
    def read(self) -> Dict[str, float]:
        self.value += self.step_delta
        return {self.value_type: self.value}
    
    def get_metadata(self) -> Dict[str, Any]:
        return {"type": "temperature", "unit": "celsius"}
    
    def get_value_types(self) -> List[str]:
        return [self.value_type]
    
    def get_units(self) -> Dict[str, str]:
        return {self.value_type: "celsius"}

@pytest.fixture
def simulation_env():
    # Create environment with shorter duration for testing
    env = SimulationEnvironment()
    env.duration = 3600  # 1 hour
    env.timestep = 300   # 5 minutes
    return env

@pytest.fixture
def agent():
    return LLMAgent()

@pytest.fixture
def strategy():
    return EnergyOptimizationStrategy()

def test_full_simulation_run(simulation_env, agent):
    """Test a full simulation run with actual components."""
    # Add test devices
    simulation_env.add_device("temperature", TestDevice(20.0, 0.1))
    simulation_env.add_device("humidity", TestDevice(45.0, 0.2))
    simulation_env.add_device("energy_consumption", TestDevice(1.0, 0.05))
    
    # Add agent
    simulation_env.add_agent(agent)
    
    # Run simulation
    history = simulation_env.run()
    
    # Verify simulation completed successfully
    assert len(history) > 0
    assert simulation_env.current_time >= simulation_env.duration
    
    # Check that state history contains expected data
    for state in history:
        assert "timestamp" in state
        assert "devices" in state
        assert all(device in state["devices"] 
                  for device in ["temperature", "humidity", "energy_consumption"])

def test_agent_strategy_integration(simulation_env, agent, strategy):
    """Test integration between agent and strategy components."""
    # Add test device
    simulation_env.add_device("temperature", TestDevice(20.0, 0.1))
    
    # Add agent
    simulation_env.add_agent(agent)
    
    # Run for a few steps
    for _ in range(5):
        state = simulation_env.step()
        
        # Evaluate state with strategy
        score = strategy.evaluate(state)
        suggestion = strategy.suggest(state)
        
        # Verify basic integration
        assert 0 <= score <= 1
        assert isinstance(suggestion, dict)
        assert "action" in suggestion
