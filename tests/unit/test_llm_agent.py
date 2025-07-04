import pytest
import time
from core.agents.llm_agent_mistral import LLMAgentMistral
from core.agents.llm_agent_mistral_magyar_jetson import LLMAgentMistralMagyarJetson
from core.agents.llm_agent_phi2 import LLMAgentPhi2
from core.agents.llm_agent_falcon_rw_1b import LLMAgentFalconRW1B
from core.agents.llm_agent_tinyllama import LLMAgentTinyLlama

QUESTIONS = [
    "Explain in 20 words what temperature is.",
    "Tell in 20 words how can I optimize energy usage?",
    # "What is the weather forecast for tomorrow?",
    # "Summarize the benefits of solar panels.",
    # "How do I reset my smart thermostat?"
]

@pytest.mark.parametrize("AgentClass,agent_name", [
    # (LLMAgentMistral, "Mistral-7B-Instruct-v0.3"),
    # (LLMAgentMistralMagyarJetson, "MistralMagyarJetson"),
    (LLMAgentPhi2, "Phi2"),
    (LLMAgentFalconRW1B, "FalconRW1B"),
    (LLMAgentTinyLlama, "TinyLlama"),
])
def test_llm_agent_ask_multiple_questions_and_time(AgentClass, agent_name):
    agent = AgentClass()
    times = []
    print(f"\nTesting agent: {agent_name}")
    for q in QUESTIONS:
        start = time.time()
        result = agent.ask(q)
        elapsed = time.time() - start
        times.append(elapsed)
        assert isinstance(result, str)
        chars = len(result)
        time_per_char = elapsed / chars if chars > 0 else 0
        print(f"Question: {q}\nResponse: {result}\nTime: {elapsed:.2f} seconds ({time_per_char:.4f} s/char)\n")
    print(f"All response times for {agent_name}: {times}\n")
