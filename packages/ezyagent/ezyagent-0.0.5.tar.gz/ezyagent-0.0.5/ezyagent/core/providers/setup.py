from typing import Any
from openai import AsyncOpenAI
from ezyagent.utils.errors import AgentError
from .config import ProviderConfig
from .registry import ProviderRegistry

class ProviderSetup:
    """Main class for setting up LLM providers"""
    def __init__(self, registry: ProviderRegistry):
        self.registry = registry

    def _get_provider_name(self, config: ProviderConfig) -> str:
        """Extract provider name from config"""
        if config.provider is not None:
            return config.provider
        return config.model.split(":")[0] if ':' in config.model else "openai"

    def setup_provider(self, config: ProviderConfig, **kwargs: Any) -> AsyncOpenAI:
        """Set up the LLM provider"""
        try:
            provider_name = self._get_provider_name(config)
            factory = self.registry.get_factory(provider_name)
            return factory.create_client(config, **kwargs)
        except Exception as e:
            raise AgentError(f"Failed to initialize provider {provider_name}: {str(e)}")