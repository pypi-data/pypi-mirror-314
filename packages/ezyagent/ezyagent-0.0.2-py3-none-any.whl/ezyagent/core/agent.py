import asyncio
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from .providers.base import BaseProvider, Message, ProviderResponse
from ..logging.logger import AgentLogger
from ..utils.errors import AgentError


class Tool(BaseModel):
    """Tool definition."""
    name: str
    description: str
    function: Callable
    is_async: bool = True
    parameters: Dict[str, Any] = Field(default_factory=dict)


class Agent:
    """Main agent class for interacting with LLMs."""

    def __init__(
        self,
        model: str = "gpt-4",
        provider: Optional[Union[str, BaseProvider]] = None,
        api_key: Optional[str] = None,
        **kwargs: Any
    ):
        """Initialize the agent.

        Args:
            model: Model identifier (e.g., "gpt-4", "claude-2")
            provider: Provider name or instance ("openai", "anthropic", etc.)
            api_key: API key for the provider
            **kwargs: Additional provider-specific arguments
        """
        self.model = model
        self.provider = self._setup_provider(provider, api_key, **kwargs)
        self.tools: Dict[str, Tool] = {}
        self.logger = AgentLogger()

    def _setup_provider(
        self,
        provider: Optional[Union[str, BaseProvider]],
        api_key: Optional[str],
        **kwargs: Any
    ) -> BaseProvider:
        """Set up the LLM provider."""
        if isinstance(provider, BaseProvider):
            return provider

        provider_name = provider or "openai"  # Default to OpenAI

        try:
            if provider_name == "openai":
                from .providers.openai import OpenAIProvider
                return OpenAIProvider(api_key=api_key, **kwargs)
            elif provider_name == "anthropic":
                from .providers.anthropic import AnthropicProvider
                return AnthropicProvider(api_key=api_key, **kwargs)
            elif provider_name == "ollama":
                from .providers.ollama import OllamaProvider
                return OllamaProvider(**kwargs)
            else:
                raise ValueError(f"Unsupported provider: {provider_name}")
        except Exception as e:
            raise AgentError(f"Failed to initialize provider {provider_name}: {str(e)}")

    def tool(self, func: Optional[Callable] = None, **kwargs: Any) -> Callable:
        """Decorator to register a tool."""

        def decorator(func: Callable) -> Callable:
            tool_name = kwargs.get('name', func.__name__)
            self.tools[tool_name] = Tool(
                name=tool_name,
                description=func.__doc__ or "No description provided",
                function=func,
                is_async=asyncio.iscoroutinefunction(func),
                parameters=kwargs.get('parameters', {})
            )
            return func

        return decorator if func is None else decorator(func)

    async def chat(
        self,
        message: str,
        stream: bool = False,
        **kwargs: Any
    ) -> Union[str, AsyncIterator[str]]:
        """Send a message to the agent.

        Args:
            message: User message
            stream: Whether to stream the response
            **kwargs: Additional arguments for the provider

        Returns:
            Agent's response as string or async iterator of strings if streaming
        """
        try:
            messages = [Message(role="user", content=message)]

            with self.logger.span("agent.chat") as span:
                span.set_tag("message", message)

                response = await self.provider.chat(
                    messages=messages,
                    stream=stream,
                    **kwargs
                )

                if stream:
                    return self._handle_streaming_response(response)
                else:
                    return self._handle_response(response)

        except Exception as e:
            self.logger.error("Chat failed", error=str(e))
            raise AgentError(f"Chat failed: {str(e)}")

    async def _handle_streaming_response(
        self,
        response: AsyncIterator[ProviderResponse]
    ) -> AsyncIterator[str]:
        """Handle streaming response from provider."""
        async for chunk in response:
            yield chunk.content

    def _handle_response(self, response: ProviderResponse) -> str:
        """Handle non-streaming response from provider."""
        return response.content

    async def arun_tool(self, tool_name: str, **kwargs: Any) -> Any:
        """Run a tool asynchronously."""
        if tool_name not in self.tools:
            raise AgentError(f"Tool not found: {tool_name}")

        tool = self.tools[tool_name]
        try:
            if tool.is_async:
                return await tool.function(**kwargs)
            else:
                return tool.function(**kwargs)
        except Exception as e:
            raise AgentError(f"Tool execution failed: {str(e)}")

    async def __aenter__(self) -> 'Agent':
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        # Cleanup code here if needed
        pass