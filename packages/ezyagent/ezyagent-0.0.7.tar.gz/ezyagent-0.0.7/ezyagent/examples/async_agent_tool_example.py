import asyncio
import os

from ezyagent import AgentLogger

os.environ['OPENAI_API_KEY'] = "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"
from ezyagent.core.agents.base import BaseAgent
from ezyagent.core.agents.agent import Agent


# Define some example tools
def calculator(expression: str) -> float:
    """A simple calculator that evaluates mathematical expressions."""
    return eval(expression)


def weather(city: str) -> str:
    """Get weather information for a city (mock implementation)."""
    return f"The weather in {city} is sunny and 22°C"


logger = AgentLogger(level='CRITICAL')

async def main():
    # Example 1: Basic Agent without tools
    print("\n=== Example 1: Basic Agent ===")
    agent = BaseAgent(model="huggingface:01-ai/Yi-1.5-34B-Chat",
                      logger=logger)
    async for chunk in await agent.chat("2+3?", stream=True):
        print(chunk, end="")

    # Example 2: Agent with tools using decorator
    print("\n\n=== Example 2: Agent with Decorated Tools ===")
    tool_agent = Agent(model="huggingface:01-ai/Yi-1.5-34B-Chat",
                       logger=logger)

    @tool_agent.tool
    def greet(name: str) -> str:
        """Greet a person by name."""
        print('GREEEEEETINGGGG')
        return f"Hello, {name}!"

    message = "My name is Alice. Can you greet me?"
    res = await tool_agent.chat(message)
    print(res, flush=True)

    # Example 3: Agent with tools passed directly
    print("\n\n=== Example 3: Agent with Direct Tools ===")
    direct_agent = Agent(model="huggingface:01-ai/Yi-1.5-34B-Chat",
                         logger=logger)
    message = "What's 5+7 and what's the weather in London?"

    res = await direct_agent.chat(
        message,
        extra_tools=[calculator, weather])
    print(res, end="")



    # Example 5: Combining multiple approaches
    print("\n\n=== Example 5: Combined Approach ===")
    combined_agent = Agent(model="huggingface:01-ai/Yi-1.5-34B-Chat",
                           logger=logger)

    @combined_agent.tool
    def translate(text: str, to_lang: str) -> str:
        """Translate text to specified language (mock implementation)."""
        return f"Translated '{text}' to {to_lang}"

    message = "Translate 'hello' to Spanish and tell me the weather in Paris"
    async for chunk in await combined_agent.chat(
        message,
        stream=True,
        extra_tools=[weather]
    ):
        print(chunk, end="")

async def example3():
    # Example 4: Using async context manager
    print("\n\n=== Example 4: Using Context Manager ===")
    async with Agent(model="huggingface:01-ai/Yi-1.5-34B-Chat",
                     logger=logger) as ctx_agent:
        @ctx_agent.tool
        def search(query: str) -> list[str]:
            """Search for information (mock implementation)."""
            return [f"Result for: {query}"]

        message = "Can you search for 'python programming'?"
        # async for chunk in await ctx_agent.chat(message, stream=True):
        #     print(chunk, end="")
        res = await ctx_agent.chat(message)
        print(res)
        ctx_agent.print_agent_info()


async def ex4():
    print("\n\n=== Example 3: Agent with Direct Tools ===")
    direct_agent = Agent(model="huggingface:01-ai/Yi-1.5-34B-Chat",
                         logger=logger)
    message = "what's the weather in London?"

    res = await direct_agent.chat(
        message,
        extra_tools=[calculator, weather],
        # return_tool_arguments = True
    )
    print(res, end="")
if __name__ == '__main__':
    # asyncio.run(main())
    asyncio.run(example3())
    asyncio.run(ex4())