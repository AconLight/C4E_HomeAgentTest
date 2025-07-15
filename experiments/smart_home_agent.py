
import time
from core.agents.llm_agent_tinyllama import LLMAgentTinyLlama
import requests


def read_sensor_data():
    x = requests.get('http://192.168.10.73/ms-params')
    # print(str(x.json()))
    # print(x.json().keys())
    # print(x.json()['temperature'])
    return x.json()

def create_prompt(command):
    return f"""
    Q: (Rules:
     - you are a smart home agent.
     - question reffers to sensor data (1: temperatura, 2: wilgotność, 3: ciśnienie)
     - question: {command}
     - decide what sensor data and answer immediately with only one digit
     - answer 1, 2 or 3)
    A: """


    # Q: for \'lubie placki\' return 1 if reffers to \'temperatura\', 2 if reffers to \'wilgotność\', 3 if reffers to \'ciśnienie\' , 0 if otherwise
    # A: 0
def create_prompt2(command):
    return f"""
    Q: for \'cześć jaka jest temperatura?\' return 1 if reffers to \'temperatura\', 2 if reffers to \'wilgotność\', 3 if reffers to \'ciśnienie\' , 0 if otherwise
    A: 1 - temperature
    Q: for \'jak wilgotno jest na dworze?\' return 1 if reffers to \'temperatura\', 2 if reffers to \'wilgotność\', 3 if reffers to \'ciśnienie\' , 0 if otherwise
    A: 2 - humidity
    Q: for \'jak duże jest ciśnienie\' return 1 if reffers to \'temperatura\', 2 if reffers to \'wilgotność\', 3 if reffers to \'ciśnienie\' , 0 if otherwise
    A: 3 - pressure
    Q: for \'jak ciepło jest na dworze\' return 1 if reffers to \'temperatura\', 2 if reffers to \'wilgotność\', 3 if reffers to \'ciśnienie\' , 0 if otherwise
    A: 1 - temperature
    Q: for \'jaka jest wilgotność?\' return 1 if reffers to \'temperatura\', 2 if reffers to \'wilgotność\', 3 if reffers to \'ciśnienie\' , 0 if otherwise
    A: 2 - humidity
    Q: for \'jakie jest ciśnienie\' return 1 if reffers to \'temperatura\', 2 if reffers to \'wilgotność\', 3 if reffers to \'ciśnienie\' , 0 if otherwise
    A: 3 - pressure
    FINAL Q&A
    Q: for \'{command}\' return 0, 1, 2, or 3
    A: """

def create_prompt_from_data(data, question):
    return f"""
    FINAL Q&A
    Q: Based on sensor data: ({data}) tell me {question}
    A: """


def test_smart_home_agent(AgentClass, agent_name):
    agent = AgentClass()
    print(f"\nTesting smart home agent: {agent_name}\nJak mogę pomóc?")
    while(True):
        command = input()
        prompt = create_prompt2(command)
        result = agent.ask(prompt)
        char_digit = result[len(prompt)-5]
        # print(result)
        print(f'[log] char_digit: {char_digit}')
        if char_digit == "1":
            sensor_data = read_sensor_data()['temperature']
            print(f"temperatura wynosi {sensor_data}")
        elif char_digit == "2":
            sensor_data = read_sensor_data()['humidity']
            print(f"wilgotność powietrza wynosi {sensor_data}")
        elif char_digit == "3":
            sensor_data = read_sensor_data()['pressure']
            print(f"ciśnienie powietrza wynosi {sensor_data}")
        else:
            print("przetwarzam pytanie...")
            sensor_data = read_sensor_data()
            prompt = create_prompt_from_data(str(sensor_data), command)
            result = agent.ask(prompt)
            print(result[len(prompt)-1:])

def test_smart_home_agent_from_data(AgentClass, agent_name):
    agent = AgentClass()
    sensor_data = read_sensor_data()
    print(f"\nTesting smart home agent: {agent_name}\nJak mogę pomóc?")
    while(True):
        command = input()
        result = agent.ask(create_prompt_from_data(str(sensor_data), command))
        print(result)

# read_sensor_data()
test_smart_home_agent(LLMAgentTinyLlama, "TinyLlama")