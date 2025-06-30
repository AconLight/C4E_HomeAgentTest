import pytest
from unittest.mock import MagicMock
from typing import Dict, List, Any
from core.simulation.environment import SimulationEnvironment
from core.interfaces.base import Device, Agent

class MockDevice(Device):
    def __init__(self, value=20.0):
        self.value = value
    
    def read(self) -> Dict[str, float]:
        return {"test": self.value}
    
    def get_metadata(self) -> Dict[str, Any]:
        return {"type": "mock", "unit": "test"}
    
    def get_value_types(self) -> List[str]:
        return ["test"]
    
    def get_units(self) -> Dict[str, str]:
        return {"test": "unit"}

class MockAgent(Agent):
    def __init__(self):
        self.observations = []
        self.actions = []
    
    def observe(self, state):
        self.observations.append(state)
    
    def decide(self):
        return {"action": "test"}
    
    def act(self, action):
        self.actions.append(action)
        return True

@pytest.fixture
def env():
    return SimulationEnvironment()

@pytest.fixture
def mock_device():
    return MockDevice()

@pytest.fixture
def mock_agent():
    return MockAgent()

def test_environment_initialization(env):
    """Test environment initialization with default values."""
    assert env.timestep == 300  # 5 minutes
    assert env.duration == 86400  # 24 hours
    assert env.current_time == 0
    assert len(env.devices) == 0
    assert len(env.agents) == 0
    assert len(env.state_history) == 0

def test_add_device(env, mock_device):
    """Test adding a device to the environment."""
    env.add_device("test_device", mock_device)
    assert "test_device" in env.devices
    assert env.devices["test_device"] == mock_device

def test_add_agent(env, mock_agent):
    """Test adding an agent to the environment."""
    env.add_agent(mock_agent)
    assert mock_agent in env.agents
    assert len(env.agents) == 1

# def test_get_state(env, mock_sensor):
#     """Test getting current environment state."""
#     env.add_sensor("test_sensor", mock_sensor)
#     state = env.get_state()
    
#     assert "timestamp" in state
#     assert "sensors" in state
#     assert "test_sensor" in state["sensors"]
#     assert state["sensors"]["test_sensor"] == mock_sensor.read()

# def test_step(env, mock_agent, mock_sensor):
#     """Test environment step."""
#     env.add_sensor("test_sensor", mock_sensor)
#     env.add_agent(mock_agent)
    
#     initial_time = env.current_time
#     state = env.step()
    
#     # Check time advancement
#     assert env.current_time == initial_time + env.timestep
    
#     # Check state recording
#     assert len(env.state_history) == 1
#     assert env.state_history[0] == state
    
#     # Check agent interaction
#     assert len(mock_agent.observations) == 1
#     assert len(mock_agent.actions) == 1

# def test_run(env, mock_agent, mock_sensor):
#     """Test full simulation run."""
#     env.add_sensor("test_sensor", mock_sensor)
#     env.add_agent(mock_agent)
    
#     history = env.run()
    
#     # Check simulation completed
#     assert env.current_time >= env.duration
#     assert len(history) > 0
#     assert len(mock_agent.observations) == len(history)
#     assert len(mock_agent.actions) == len(history)

# def test_reset(env, mock_agent, mock_sensor):
#     """Test environment reset."""
#     env.add_sensor("test_sensor", mock_sensor)
#     env.add_agent(mock_agent)
    
#     # Run some steps
#     env.step()
#     env.step()
    
#     # Reset
#     env.reset()
    
#     assert env.current_time == 0
#     assert len(env.state_history) == 0
