import asyncio
from ezyagent.core.agents.base import BaseAgent


class CustomAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        model="huggingface:01-ai/Yi-1.5-34B-Chat"
        api_key = "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"
        super().__init__(model=model,api_key=api_key,*args, **kwargs)

async def main():
    agent = CustomAgent()

    # For streaming chat
    async for chunk in await agent.chat("2+3?",
                                         stream=True,
                                         ):
        print(chunk, end="")

    agent.print_agent_info()


    # For regular chat
    # response = await agent.chat("How can you help me?")
    # print(response)


if __name__ == '__main__':
    asyncio.run(main())