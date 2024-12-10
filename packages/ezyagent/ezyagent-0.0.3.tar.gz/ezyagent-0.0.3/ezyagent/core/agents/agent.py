import asyncio
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Union, Iterable, Literal

import httpx
from openai import OpenAI, AsyncOpenAI, NotGiven, NOT_GIVEN
from openai._types import Headers, Query, Body
from openai.types import ChatModel
from openai.types.chat import ChatCompletionChunk, ChatCompletion, ChatCompletionMessageParam, ChatCompletionAudioParam, \
    ChatCompletionModality, ChatCompletionPredictionContentParam, ChatCompletionStreamOptionsParam, \
    ChatCompletionToolChoiceOptionParam, ChatCompletionToolParam, completion_create_params
from pydantic import BaseModel, Field

from ezyagent.core.providers.base import BaseProvider, Message, ProviderResponse
from ezyagent.logging.logger import AgentLogger
from ezyagent.utils.errors import AgentError
from .._types._huggingface import HFModelType


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
        model: HFModelType = "openai:gpt-4o-mini",
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
        self.provider = self._setup_provider(provider, base_url, api_key, model, **kwargs)
        self.tools: Dict[str, Tool] = {}
        self.logger = AgentLogger()

    def _setup_provider(
        self,
        provider: Optional[Union[str, BaseProvider]],
        base_url: Optional[str],
        api_key: Optional[str],
        model: str,
        **kwargs: Any
    ) -> OpenAI | AsyncOpenAI:
        """Set up the LLM provider."""

        if provider is None:
            provider_name = model.split(":")[0] if ':' in model else "openai"
        else:
            provider_name = provider or "openai"  # Default to OpenAI

        if provider_name is None:
            raise ValueError("Model provider name must be provided or model as provider:modelname")

        try:
            if provider_name == "openai":
                return OpenAI(api_key=api_key, **kwargs)
            elif provider_name in ["ollama", "huggingface"]:
                if base_url is None:
                    if provider_name == "huggingface":
                        base_url: str = "https://api-inference.huggingface.co/v1/"
                    else:
                        base_url: str = 'http://localhost:11434/v1'
                        api_key = 'ollama'  # required, but unused
                return OpenAI(base_url=base_url, api_key=api_key, **kwargs)
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

    def chat(
        self,
        messages: Iterable[ChatCompletionMessageParam]|str,
        model: Union[str, ChatModel]=None,
        *,
        stream: bool = False,
        audio: Optional[ChatCompletionAudioParam] | NotGiven = NOT_GIVEN,
        frequency_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        function_call: completion_create_params.FunctionCall | NotGiven = NOT_GIVEN,
        functions: Iterable[completion_create_params.Function] | NotGiven = NOT_GIVEN,
        logit_bias: Optional[Dict[str, int]] | NotGiven = NOT_GIVEN,
        logprobs: Optional[bool] | NotGiven = NOT_GIVEN,
        max_completion_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        max_tokens: Optional[int] | NotGiven = NOT_GIVEN,
        metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        modalities: Optional[List[ChatCompletionModality]] | NotGiven = NOT_GIVEN,
        n: Optional[int] | NotGiven = NOT_GIVEN,
        parallel_tool_calls: bool | NotGiven = NOT_GIVEN,
        prediction: Optional[ChatCompletionPredictionContentParam] | NotGiven = NOT_GIVEN,
        presence_penalty: Optional[float] | NotGiven = NOT_GIVEN,
        response_format: completion_create_params.ResponseFormat | NotGiven = NOT_GIVEN,
        seed: Optional[int] | NotGiven = NOT_GIVEN,
        service_tier: Optional[Literal["auto", "default"]] | NotGiven = NOT_GIVEN,
        stop: Union[Optional[str], List[str]] | NotGiven = NOT_GIVEN,
        store: Optional[bool] | NotGiven = NOT_GIVEN,
        stream_options: Optional[ChatCompletionStreamOptionsParam] | NotGiven = NOT_GIVEN,
        temperature: Optional[float] | NotGiven = NOT_GIVEN,
        tool_choice: ChatCompletionToolChoiceOptionParam | NotGiven = NOT_GIVEN,
        tools: Iterable[ChatCompletionToolParam] | NotGiven = NOT_GIVEN,
        top_logprobs: Optional[int] | NotGiven = NOT_GIVEN,
        top_p: Optional[float] | NotGiven = NOT_GIVEN,
        user: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        **kwargs: Any
    ) -> Union[str, AsyncIterator[str]]:
        """Send a message to the agent.

        Args:
            prompt: User message
            messages: List of messages in the conversation
            stream: Whether to stream the response
            **kwargs: Additional arguments for the provider

        Returns:
            Agent's response as string or async iterator of strings if streaming
        """
        try:
            model = model or self.model
            if isinstance(messages,str):
                messages = [Message(role="user", content=messages)]

            with self.logger.span("agent.chat") as span:
                span.set_tag("message", messages)

                response = self.provider.chat.completions.create(
                    messages=messages,
                    model=model,
                    stream=stream,
                    audio=audio,
                    frequency_penalty=frequency_penalty,
                    function_call=function_call,
                    functions=functions,
                    logit_bias=logit_bias,
                    logprobs=logprobs,
                    max_completion_tokens=max_completion_tokens,
                    max_tokens=max_tokens,
                    metadata=metadata,
                    modalities=modalities,
                    n=n,
                    parallel_tool_calls=parallel_tool_calls,
                    prediction=prediction,
                    presence_penalty=presence_penalty,
                    response_format=response_format,
                    seed=seed,
                    service_tier=service_tier,
                    stop=stop,
                    store=store,
                    stream_options=stream_options,
                    temperature=temperature,
                    tool_choice=tool_choice,
                    tools=tools,
                    top_logprobs=top_logprobs,
                    top_p=top_p,
                    user=user,
                    extra_headers=extra_headers,
                    extra_query=extra_query,
                    extra_body=extra_body,
                    timeout=timeout,
                    **kwargs,
                )

                if stream:
                    return self._handle_streaming_response(response)
                else:
                    return self._handle_response(response)

        except Exception as e:
            self.logger.error("Chat failed", error=str(e))
            raise AgentError(f"Chat failed: {str(e)}")

    def _handle_streaming_response(
        self,
        response: Iterable[ChatCompletionChunk]
    ) -> str:
        """Handle streaming response from provider."""
        for chunk in response:
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

    def _get_model(self, model:str):
        return model.split(":", 1)[1]