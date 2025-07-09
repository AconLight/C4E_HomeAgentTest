
import time
from core.agents.llm_agent_tinyllama import LLMAgentTinyLlama

QUESTIONS = [
    "Explain in 20 words what temperature is, I want",
    "Tell in 20 words how can I optimize energy usage? what is",
    # "What is the weather forecast for tomorrow?",
    # "Summarize the benefits of solar panels.",
    # "How do I reset my smart thermostat?"
]

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

test_llm_agent_ask_multiple_questions_and_time(LLMAgentTinyLlama, "TinyLlama")