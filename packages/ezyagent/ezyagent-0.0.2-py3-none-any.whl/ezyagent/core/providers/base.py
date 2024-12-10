from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, List, Optional, Union
import asyncio
from pydantic import BaseModel, Field


class CompletionChoice(BaseModel):
    """Represents a completion choice from the model."""
    index: int = 0
    text: str
    finish_reason: Optional[str] = None
    logprobs: Optional[Dict[str, Any]] = None


class UsageInfo(BaseModel):
    """Token usage information."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ProviderResponse(BaseModel):
    """Standardized response from providers."""
    content: str
    raw_response: Any
    usage: UsageInfo
    finish_reason: Optional[str] = None
    model: str
    provider_name: str


class FunctionCall(BaseModel):
    """Function call information."""
    name: str
    arguments: Dict[str, Any]
    description: Optional[str] = None


class Message(BaseModel):
    """Message class for standardizing communication."""
    role: str
    content: str
    name: Optional[str] = None
    function_call: Optional[FunctionCall] = None


class ModelConfig(BaseModel):
    """Model configuration."""
    model_name: str
    max_tokens: Optional[int] = None
    temperature: float = 0.7
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop: Optional[List[str]] = None
    functions: Optional[List[Dict[str, Any]]] = None


class BaseProvider(ABC):
    """Base class for all LLM providers."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 60,
        max_retries: int = 3,
        **kwargs: Any
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.kwargs = kwargs
        self._session: Optional[Any] = None
        self._validate_credentials()

    @abstractmethod
    def _validate_credentials(self) -> None:
        """Validate API credentials."""
        pass

    @abstractmethod
    async def create_session(self) -> None:
        """Create an HTTP session."""
        pass

    @abstractmethod
    async def close_session(self) -> None:
        """Close the HTTP session."""
        pass

    @abstractmethod
    async def chat(
        self,
        messages: List[Message],
        model_config: Optional[ModelConfig] = None,
        stream: bool = False,
        **kwargs: Any
    ) -> Union[ProviderResponse, AsyncIterator[ProviderResponse]]:
        """Send a chat request to the provider."""
        pass

    @abstractmethod
    async def generate_embedding(
        self,
        text: str,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> List[float]:
        """Generate embeddings for the given text."""
        pass

    @abstractmethod
    async def get_token_count(self, text: str, model: Optional[str] = None) -> int:
        """Get token count for the given text."""
        pass

    @abstractmethod
    def get_model_context_size(self, model: str) -> int:
        """Get the context size for the given model."""
        pass

    @abstractmethod
    async def validate_response(self, response: Any) -> None:
        """Validate provider response."""
        pass

    async def aclose(self) -> None:
        """Close the provider session."""
        if self._session:
            await self.close_session()

    async def __aenter__(self) -> 'BaseProvider':
        """Async context manager entry."""
        await self.create_session()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.aclose()