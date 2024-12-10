from typing import Any
from openai import AsyncOpenAI
from ..base import ProviderFactory
from ..config import ProviderConfig

class OpenAIProviderFactory(ProviderFactory):
    """Factory for OpenAI provider"""
    def create_client(self, config: ProviderConfig, **kwargs: Any) -> AsyncOpenAI:
        return AsyncOpenAI(api_key=config.api_key, **kwargs)