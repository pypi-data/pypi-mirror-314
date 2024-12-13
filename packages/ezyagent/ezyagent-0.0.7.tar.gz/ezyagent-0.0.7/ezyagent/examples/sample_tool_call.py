import asyncio
import os

from ezyagent import Agent, AgentLogger

os.environ['OPENAI_API_KEY'] = "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"

#tools
def calculator(expression: str) -> float:
    """A simple calculator that evaluates mathematical expressions."""
    return eval(expression)

def weather(city: str) -> str:
    """Get weather information for a city (mock implementation)."""
    return f"The weather in {city} is sunny and 22°C"


async def main():
    # agent = Agent(model="huggingface:01-ai/Yi-1.5-34B-Chat",
    #                      logger=AgentLogger(level='CRITICAL'))

    agent = Agent(model="ollama:qwen2.5:7b-instruct",
                         base_url="http://192.168.170.76:11434/v1",
                         logger=AgentLogger(level='DEBUG'))

    res = await agent.chat(messages="what's the weather in London?",
                                  extra_tools=[calculator, weather],
                                  # return_tool_arguments = True
                                  )

    print(res)

if __name__ == '__main__':
    asyncio.run(main())