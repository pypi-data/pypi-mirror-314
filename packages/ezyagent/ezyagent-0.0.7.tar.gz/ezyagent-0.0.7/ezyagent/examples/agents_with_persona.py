import asyncio

from ezyagent import Agent, AgentLogger


def weather(city: str) -> str:
    """Get weather information for a city (mock implementation)."""
    return f"The weather in {city} is sunny and 22°C"


async def main():
    agent = Agent(model="ollama:qwen2.5:7b-instruct",
                         base_url="http://192.168.170.76:11434/v1",
                         logger=AgentLogger(level='INFO'))

    persona = agent("""You are weather expert""")

    res = await persona("tell me weather in newyork",
                        model="qwen2.5:1.5b-instruct",
                        extra_tools = [weather])

    #or
    messages = [
        {"role":"system","content":"""You are weather expert"""},
        {"role":"user","content":"tell me weather in newyork"}
    ]
    res = await agent.chat(messages=messages,
                                  extra_tools=[weather])

    print(res) #AgentResult(type='tool_result', content='The weather in New York is sunny and 22°C', tool_arguments='{"city":"New York"}', tool_name='weather')


if __name__ == '__main__':
    asyncio.run(main())