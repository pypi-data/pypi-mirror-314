from abc import ABC, abstractmethod
from typing import Any
from openai import AsyncOpenAI
from .config import ProviderConfig

class ProviderFactory(ABC):
    """Abstract factory for creating provider clients"""
    @abstractmethod
    def create_client(self, config: ProviderConfig, **kwargs: Any) -> AsyncOpenAI:
        """Create a provider client"""
        pass