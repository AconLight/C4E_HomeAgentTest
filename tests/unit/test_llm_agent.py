import pytest
from typing import Dict, Any
from core.agents.llm_agent import LLMAgent

@pytest.fixture
def agent():
    return LLMAgent()

def test_agent_initialization(agent):
    """Test that agent initializes correctly."""
    assert isinstance(agent.state_history, list)
    assert len(agent.state_history) == 0

def test_agent_observe(agent):
    """Test that agent can observe and store state."""
    test_state = {
        "timestamp": 1000,
        "sensors": {
            "temperature": 22.5,
            "humidity": 45
        }
    }
    
    agent.observe(test_state)
    assert len(agent.state_history) == 1
    assert agent.state_history[0] == test_state
    
    # Test history limit
    for i in range(150):
        agent.observe({"timestamp": i})
    assert len(agent.state_history) <= 100

def test_agent_decide_normal_temp(agent):
    """Test agent decision with normal temperature."""
    test_state = {
        "timestamp": 1000,
        "sensors": {
            "temperature": 22.5
        }
    }
    agent.observe(test_state)
    
    action = agent.decide()
    assert action == {"action": "maintain"}

def test_agent_decide_high_temp(agent):
    """Test agent decision with high temperature."""
    test_state = {
        "timestamp": 1000,
        "sensors": {
            "temperature": 25.0
        }
    }
    agent.observe(test_state)
    
    action = agent.decide()
    assert action == {"action": "cool_down"}

def test_agent_decide_low_temp(agent):
    """Test agent decision with low temperature."""
    test_state = {
        "timestamp": 1000,
        "sensors": {
            "temperature": 19.0
        }
    }
    agent.observe(test_state)
    
    action = agent.decide()
    assert action == {"action": "heat_up"}

def test_agent_decide_no_temp(agent):
    """Test agent decision without temperature data."""
    test_state = {
        "timestamp": 1000,
        "sensors": {
            "humidity": 45
        }
    }
    agent.observe(test_state)
    
    action = agent.decide()
    assert action == {"action": "maintain"}

def test_agent_act(agent):
    """Test agent action execution."""
    test_action = {"action": "test_action"}
    result = agent.act(test_action)
    assert isinstance(result, bool)

def test_state_history_limit(agent):
    """Test that state history is limited to 100 entries."""
    for i in range(150):
        agent.observe({"timestamp": i})
    assert len(agent.state_history) == 100
    assert agent.state_history[0]["timestamp"] == 50

def test_ask_method_returns_string(agent):
    """Test that the ask method takes a string and returns a string."""
    result = agent.ask("What is the temperature?")
    assert isinstance(result, str)
