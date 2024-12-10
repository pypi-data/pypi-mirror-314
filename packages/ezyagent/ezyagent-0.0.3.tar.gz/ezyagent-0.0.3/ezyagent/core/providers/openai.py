from typing import Any, AsyncIterator, Dict, List, Optional, Union
from openai import AsyncOpenAI
from .base import (
    BaseProvider,
    Message,
    ModelConfig,
    ProviderResponse,
    UsageInfo,
)


class OpenAIProvider(BaseProvider):
    """Provider class for OpenAI API integration using official client."""

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: int = 60,
        max_retries: int = 3,
        organization: Optional[str] = None,
        **kwargs: Any
    ):
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            **kwargs
        )
        self.organization = organization
        self._openai_client: Optional[AsyncOpenAI] = None

    def _validate_credentials(self) -> None:
        """Validate OpenAI credentials."""
        if not self.api_key:
            raise ValueError("OpenAI API key is required")

    async def create_session(self) -> None:
        """Create OpenAI AsyncClient."""
        self._openai_client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
            max_retries=self.max_retries,
            organization=self.organization,
            **self.kwargs
        )
        self._session = self._openai_client  # For base provider compatibility

    async def close_session(self) -> None:
        """Close the OpenAI client session."""
        if self._openai_client:
            await self._openai_client.close()

    def _convert_to_openai_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """Convert internal message format to OpenAI format."""
        openai_messages = []
        for msg in messages:
            message = {
                "role": msg.role,
                "content": msg.content
            }
            if msg.name:
                message["name"] = msg.name
            if msg.function_call:
                message["function_call"] = {
                    "name": msg.function_call.name,
                    "arguments": msg.function_call.arguments
                }
            openai_messages.append(message)
        return openai_messages

    async def chat(
        self,
        messages: List[Message],
        model_config: Optional[ModelConfig] = None,
        stream: bool = False,
        **kwargs: Any
    ) -> Union[ProviderResponse, AsyncIterator[ProviderResponse]]:
        """Send a chat request using OpenAI client."""
        if not self._openai_client:
            await self.create_session()

        model = model_config.model_name if model_config else kwargs.get("model", "gpt-3.5-turbo")

        # Prepare request parameters
        request_params = {
            "model": model,
            "messages": self._convert_to_openai_messages(messages),
            "stream": stream,
            **kwargs
        }

        # Add model configuration if provided
        if model_config:
            if model_config.temperature is not None:
                request_params["temperature"] = model_config.temperature
            if model_config.max_tokens is not None:
                request_params["max_tokens"] = model_config.max_tokens
            if model_config.top_p is not None:
                request_params["top_p"] = model_config.top_p
            if model_config.frequency_penalty is not None:
                request_params["frequency_penalty"] = model_config.frequency_penalty
            if model_config.presence_penalty is not None:
                request_params["presence_penalty"] = model_config.presence_penalty
            if model_config.stop:
                request_params["stop"] = model_config.stop
            if model_config.functions:
                request_params["functions"] = model_config.functions

        if stream:
            return self._process_streaming_response(
                await self._openai_client.chat.completions.create(**request_params),
                model
            )
        else:
            response = await self._openai_client.chat.completions.create(**request_params)
            return self._create_provider_response(response, model)

    async def _process_streaming_response(
        self,
        response: AsyncIterator[Any],
        model: str
    ) -> AsyncIterator[ProviderResponse]:
        """Process streaming responses from OpenAI."""
        async for chunk in response:
            if chunk.choices:
                content = chunk.choices[0].delta.content or ""
                yield ProviderResponse(
                    content=content,
                    raw_response=chunk,
                    usage=UsageInfo(
                        prompt_tokens=0,  # Streaming doesn't provide token counts per chunk
                        completion_tokens=0,
                        total_tokens=0
                    ),
                    finish_reason=chunk.choices[0].finish_reason,
                    model=model,
                    provider_name="openai"
                )

    def _create_provider_response(self, response: Any, model: str) -> ProviderResponse:
        """Create ProviderResponse from OpenAI response."""
        return ProviderResponse(
            content=response.choices[0].message.content,
            raw_response=response,
            usage=UsageInfo(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens
            ),
            finish_reason=response.choices[0].finish_reason,
            model=model,
            provider_name="openai"
        )

    async def generate_embedding(
        self,
        text: str,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> List[float]:
        """Generate embeddings using OpenAI client."""
        if not self._openai_client:
            await self.create_session()

        response = await self._openai_client.embeddings.create(
            model=model or "text-embedding-3-small",
            input=text,
            **kwargs
        )
        return response.data[0].embedding

    async def get_token_count(self, text: str, model: Optional[str] = None) -> int:
        """Get token count using tiktoken."""
        import tiktoken
        model = model or "gpt-3.5-turbo"
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))

    def get_model_context_size(self, model: str) -> int:
        """Get model's context size."""
        context_sizes = {
            "gpt-4": 8192,
            "gpt-4-32k": 32768,
            "gpt-4-turbo-preview": 128000,
            "gpt-3.5-turbo": 4096,
            "gpt-3.5-turbo-16k": 16384,
            "text-embedding-3-small": 8191,
            "text-embedding-3-large": 8191
        }
        return context_sizes.get(model.lower(), 4096)

    async def validate_response(self, response: Any) -> None:
        """Validate response (handled by OpenAI client)."""
        pass  # The OpenAI client handles response validation