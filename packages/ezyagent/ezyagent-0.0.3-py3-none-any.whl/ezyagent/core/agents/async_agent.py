import asyncio
from contextlib import asynccontextmanager, contextmanager
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Union, Iterable, Literal, AsyncGenerator

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
    """Main agent class for interacting with LLMs with async support."""

    def __init__(
        self,
        model: HFModelType = "openai:gpt-4o-mini",
        provider: Optional[Union[str, BaseProvider]] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any
    ):
        """Initialize the agent."""
        self.model = self._get_model(model)
        self.provider = self._setup_provider(provider, base_url, api_key, model, **kwargs)
        self.tools: Dict[str, Tool] = {}
        self.logger = AgentLogger()
        self._setup_done = False

    async def _async_init(self) -> None:
        """Async initialization tasks."""
        if not self._setup_done:
            # Any async setup tasks can go here
            self._setup_done = True

    def _setup_provider(
        self,
        provider: Optional[Union[str, BaseProvider]],
        base_url: Optional[str],
        api_key: Optional[str],
        model: str,
        **kwargs: Any
    ) -> AsyncOpenAI:
        """Set up the LLM provider."""
        if provider is None:
            provider_name = model.split(":")[0] if ':' in model else "openai"
        else:
            provider_name = provider or "openai"

        if provider_name is None:
            raise ValueError("Model provider name must be provided or model as provider:modelname")

        try:
            if provider_name == "openai":
                return AsyncOpenAI(api_key=api_key, **kwargs)
            elif provider_name in ["ollama", "huggingface"]:
                if base_url is None:
                    if provider_name == "huggingface":
                        base_url = "https://api-inference.huggingface.co/v1/"
                    else:
                        base_url = 'http://localhost:11434/v1'
                        api_key = 'ollama'
                return AsyncOpenAI(base_url=base_url, api_key=api_key, **kwargs)
            else:
                raise ValueError(f"Unsupported provider: {provider_name}")
        except Exception as e:
            raise AgentError(f"Failed to initialize provider {provider_name}: {str(e)}")

    @contextmanager
    def tool(self, func: Optional[Callable] = None, **kwargs: Any) -> Callable:
        """Context manager decorator to register a tool."""
        try:
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

            yield decorator if func is None else decorator(func)
        finally:
            # Cleanup if needed
            pass

    async def chat(
        self,
        messages: Iterable[ChatCompletionMessageParam] | str,
        model: Union[str, ChatModel] = None,
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
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        **kwargs: Any
    ) -> Union[str, AsyncIterator[str]]:
        """Async version of chat method."""
        try:
            await self._async_init()
            model = model or self.model
            if isinstance(messages, str):
                messages = [Message(role="user", content=messages)]

                self.logger.info(message=messages)

                response = await self.provider.chat.completions.create(
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
                    return await self._handle_async_response(response)

        except Exception as e:
            self.logger.error("Chat failed", error=str(e))
            raise AgentError(f"Chat failed: {str(e)}")

    async def _handle_async_response(self, response: ChatCompletion) -> str:
        """Handle async non-streaming response."""
        return response.choices[0].message.content

    async def _handle_streaming_response(
        self,
        response: AsyncIterator[ChatCompletionChunk]
    ) -> AsyncGenerator[str, None]:
        """Handle async streaming response."""
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    @asynccontextmanager
    async def session(self):
        """Async context manager for managing agent sessions."""
        try:
            await self._async_init()
            yield self
        finally:
            # Cleanup async resources if needed
            pass

    async def run_tool(self, tool_name: str, **kwargs: Any) -> Any:
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

    @asynccontextmanager
    async def tool_session(self, tool_name: str):
        """Async context manager for tool execution."""
        try:
            if tool_name not in self.tools:
                raise AgentError(f"Tool not found: {tool_name}")
            yield self.tools[tool_name]
        finally:
            # Cleanup tool-specific resources if needed
            pass

    async def __aenter__(self) -> 'Agent':
        """Async context manager entry."""
        await self._async_init()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        # Cleanup async resources here if needed
        pass

    def _get_model(self, model: str) -> str:
        """Extract model name from provider:model string."""
        return model.split(":", 1)[1]

    # Add this method to the Agent class:

    def print_agent_info(self) -> None:
        """
        Print agent information using tabulate for clean table formatting.
        """
        from tabulate import tabulate

        def format_value(value: Any) -> str:
            if isinstance(value, dict):
                return '\n'.join(f"{k}: {v}" for k, v in value.items())
            elif isinstance(value, (list, tuple)):
                return '\n'.join(str(item) for item in value)
            return str(value)

        # Collect basic configuration data
        config_data = [
            ["Model", self.model],
            ["Provider Type", type(self.provider).__name__],
            ["Setup Status", "Completed" if self._setup_done else "Pending"]
        ]

        # Print basic configuration
        print("\nAGENT CONFIGURATION")
        print(tabulate(config_data, tablefmt="grid"))

        # Collect and print tools data if any exist
        if self.tools:
            tools_data = []
            for name, tool in self.tools.items():
                tools_data.append([
                    "Name", name,
                ])
                tools_data.append([
                    "Description", tool.description
                ])
                tools_data.append([
                    "Is Async", str(tool.is_async)
                ])
                if tool.parameters:
                    tools_data.append([
                        "Parameters", format_value(tool.parameters)
                    ])
                tools_data.append(["-" * 20, "-" * 40])  # Separator between tools

            print("\nREGISTERED TOOLS")
            print(tabulate(tools_data, tablefmt="grid"))