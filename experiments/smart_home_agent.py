import time
import requests
from core.agents.llm_agent_tinyllama import LLMAgentTinyLlama

# --- Utility to fetch sensor data ---
def read_sensor_data():
    response = requests.get('http://192.168.10.73/ms-params')
    return response.json()

# --- Prompt that forces a quick classification ---
def create_sensor_classification_prompt(command):
    return f"""
You are a smart home agent. Your job is to classify questions about environmental sensor data.

Rules:
- Return 1 if the question is about temperature
- Return 2 if the question is about humidity
- Return 3 if the question is about pressure
- Return 0 if the question is unrelated

Examples:
Q: What is the pressure?
A: 3

Q: What is the humidity?
A: 2

Q: What is the temperature?
A: 1

Q: What is the humidity?
A: 2

Q: What is the current temperature?
A: 1

Q: What is the pressure?
A: 3

Q: How hot is today?
A: 1

Q: What is the humidity?
A: 2

Q: I like pancakes.
A: 0

Now classify this question:
Q: {command}
A:"""

# --- Prompt to use when full sensor data context is available ---
def create_contextual_answer_prompt(sensor_data, question):
    return f"""
You are a smart home agent. Answer the user's question based on the following sensor data:

Sensor Data:
{sensor_data}

Question:
{question}

Answer:"""

# --- Main interaction loop using classification first ---
def test_smart_home_agent(AgentClass, agent_name):
    agent = AgentClass()
    print(f"\nTesting Smart Home Agent: {agent_name}\nHow can I help you?\n")

    while True:
        command = input(">>> ")

        # Step 1: classify question
        classification_prompt = create_sensor_classification_prompt(command)
        result = agent.ask(classification_prompt)

        # Try to extract the classification digit from the response
        classification = ''.join([c for c in result if c in '0123'])[:1]

        print(f"[debug] classification: {classification}")

        # Step 2: decide what to respond with
        if classification == "1":
            sensor_value = read_sensor_data()['temperature']
            print(f"The current temperature is {sensor_value}°C.")
        elif classification == "2":
            sensor_value = read_sensor_data()['humidity']
            print(f"The current humidity is {sensor_value}%.")
        elif classification == "3":
            sensor_value = read_sensor_data()['pressure']
            print(f"The current air pressure is {sensor_value} hPa.")
        else:
            print("Analyzing your question...")
            sensor_data = read_sensor_data()
            contextual_prompt = create_contextual_answer_prompt(sensor_data, command)
            result = agent.ask(contextual_prompt)
            print(result.strip())

# --- Optional: direct QA without classification ---
def test_smart_home_agent_from_data(AgentClass, agent_name):
    agent = AgentClass()
    sensor_data = read_sensor_data()
    print(f"\nTesting Smart Home Agent (Contextual Mode): {agent_name}\nHow can I help you?\n")

    while True:
        command = input(">>> ")
        result = agent.ask(create_contextual_answer_prompt(sensor_data, command))
        print(result.strip())

# --- Start the test ---
test_smart_home_agent(LLMAgentTinyLlama, "TinyLlama")

