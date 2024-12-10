from ezyagent.core.providers.base import ModelConfig
from ezyagent.core.providers.huggingface import HuggingFaceProvider

provider = HuggingFaceProvider(api_token="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")
messages = [{"role": "user", "content": "Tell me a story"}]
import asyncio


async def main():
    response = await provider.chat(messages, model_config=ModelConfig(model_name="Qwen/Qwen2.5-72B-Instruct"))
    print(response.content)


asyncio.run(main())
