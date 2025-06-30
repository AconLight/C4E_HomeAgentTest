import pytest
import time
from core.agents.llm_agent_mistral import LLMAgentMistral

@pytest.fixture
def agent():
    return LLMAgentMistral()

def test_ask_multiple_questions_and_time(agent):
    """Test that the ask method takes several strings, returns strings, and prints response times."""
    questions = [
        "What is the temperature?",
        "How can I optimize energy usage?",
        "What is the weather forecast for tomorrow?",
        "Summarize the benefits of solar panels.",
        "How do I reset my smart thermostat?"
    ]
    times = []
    for q in questions:
        start = time.time()
        result = agent.ask(q)
        elapsed = time.time() - start
        times.append(elapsed)
        assert isinstance(result, str)
        print(f"Question: {q}\nResponse time: {elapsed:.2f} seconds\n")
    print("All response times:", times)
