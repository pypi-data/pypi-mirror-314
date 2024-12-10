import asyncio
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Union

from openai.types.chat import ChatCompletionChunk, ChatCompletion
from pydantic import BaseModel, Field

from ezyagent.core.providers.base import BaseProvider, Message, ProviderResponse
from ezyagent.logging.logger import AgentLogger
from ezyagent.utils.errors import AgentError
from openai import OpenAI, AsyncOpenAI, base_url, Stream


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
        model: str = "openai:gpt-4o-mini",
        provider: Optional[Union[str, BaseProvider]] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any
    ):
        """Initialize the agent.

        Args:
            model: Model identifier (e.g., "openai:gpt-4o-min", "anthropic:claude-2")
            provider: Provider name or instance ("openai", "anthropic", etc.)
            api_key: API key for the provider
            **kwargs: Additional provider-specific arguments
        """
        self.model = self._get_model(model)
        self.provider = self._setup_provider(provider, base_url,api_key,model,**kwargs)
        self.tools: Dict[str, Tool] = {}
        self.logger = AgentLogger()

    def _setup_provider(
        self,
        provider: Optional[Union[str, BaseProvider]],
        base_url: Optional[str],
        api_key: Optional[str],
        model:str,
        **kwargs: Any
    ) -> OpenAI | AsyncOpenAI:
        """Set up the LLM provider."""

        if provider is None:
            provider_name = model.split(":")[0] if ':' in model else "openai"
        else:
            provider_name = provider or "openai"  # Default to OpenAI

        if provider_name is None:
            raise ValueError("Model provider name  must be provided or model as provider:modelname")

        try:
            if provider_name == "openai":
                return OpenAI(api_key=api_key, **kwargs)
            elif provider_name in ["ollama","huggingface"]:
                if base_url is None:
                    if provider_name == "huggingface":
                        base_url:str = "https://api-inference.huggingface.co/v1/"
                    else:
                        base_url:str = 'http://localhost:11434/v1'
                        api_key = 'ollama',  # required, but unused
                return OpenAI(base_url=base_url,api_key=api_key,**kwargs)
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
        prompt: Optional[str] = None,
        messages: Optional[str] = None,
        stream: bool = False,
        **kwargs: Any
    ) -> Union[str,AsyncIterator[str]]:
        """Send a message to the agent.

        Args:
            message: User message
            stream: Whether to stream the response
            **kwargs: Additional arguments for the provider

        Returns:
            Agent's response as string or async iterator of strings if streaming
        """
        try:
            if prompt:
                messages = [Message(role="user", content=prompt)]
            if isinstance(messages,Dict):
                messages = [Message(role=r, content=v) for r,v in messages.items()]
            with self.logger.span("agent.chat") as span:
                span.set_tag("message", messages)

                response = await self.provider.chat.completions.create(
                    messages=messages,
                    stream=stream,
                    model=self.model,
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
        response: AsyncIterator[ChatCompletionChunk]
    ) -> AsyncIterator[str]:
        """Handle streaming response from provider."""
        async for chunk in response:
            yield chunk.choices[0].delta.content

    def _handle_response(self, response: ChatCompletion) -> str:
        """Handle non-streaming response from provider."""
        return response.choices[0].message.content

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

    def _get_model(self, model):
        return model.split(":",1)[1]