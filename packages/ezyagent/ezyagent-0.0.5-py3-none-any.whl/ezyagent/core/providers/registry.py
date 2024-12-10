from typing import Dict
from .base import ProviderFactory
from .factories.openai import OpenAIProviderFactory
from .factories.ollama import OllamaProviderFactory
from .factories.huggingface import HuggingFaceProviderFactory

class ProviderRegistry:
    """Registry for provider factories"""
    def __init__(self):
        self._factories: Dict[str, ProviderFactory] = {
            "openai": OpenAIProviderFactory(),
            "ollama": OllamaProviderFactory(),
            "huggingface": HuggingFaceProviderFactory()
        }

    def register_provider(self, name: str, factory: ProviderFactory) -> None:
        """Register a new provider factory"""
        self._factories[name] = factory

    def get_factory(self, name: str) -> ProviderFactory:
        """Get a provider factory by name"""
        if name not in self._factories:
            raise ValueError(f"Unsupported provider: {name}")
        return self._factories[name]