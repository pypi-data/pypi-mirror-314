import asyncio

from ezyagent.core.providers.ollama import OllamaProvider

from ezyagent.core.memory.base import Message
from ezyagent.core.providers.base import ModelConfig

async def main():
    provider = OllamaProvider()
    response = await provider.chat(
        messages=[Message(role="user", content="Who are you?")],
        model_config=ModelConfig(
            model_name="qwen2.5:0.5b",
            max_tokens=10
        )
    )
    print(response.content)

if __name__ == '__main__':
    asyncio.run(main())
