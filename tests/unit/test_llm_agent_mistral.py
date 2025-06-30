import pytest
from typing import Dict, Any
from core.agents.llm_agent import LLMAgent
from core.agents.llm_agent_mistral import LLMAgentMistral

@pytest.fixture
def agent():
    return LLMAgentMistral()

def test_ask_method_returns_string(agent):
    """Test that the ask method takes a string and returns a string."""
    result = agent.ask("What is the temperature?")
    assert isinstance(result, str)
