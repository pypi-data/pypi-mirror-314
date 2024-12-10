import asyncio

from ezyagent import Agent

def main():
    agent = Agent("huggingface:01-ai/Yi-1.5-34B-Chat",
                  api_key="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")

    # Register a tool
    # @agent.tool
    # async def search(query: str) -> str:
    #     """Search the web."""
    #     return f"Results for: {query}"

    # Chat with streaming
    for chunk in  agent.chat("2+3?", stream=True,max_tokens=10):
        print(chunk, end="")

    # Regular chat
    # response = await agent.chat("How can you help me?")
    # print(response)


if __name__ == '__main__':
    # asyncio.run(main())
    # asyncio.run(main())
    main()