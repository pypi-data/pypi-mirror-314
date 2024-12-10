from typing import Any, AsyncIterator, Dict, List, Optional, Union
import aiohttp
from openai import AsyncOpenAI, AsyncStream
from tenacity import retry, stop_after_attempt, wait_exponential

from .base import (
    BaseProvider,
    Message,
    ModelConfig,
    ProviderResponse,
    UsageInfo,
)
from ...utils.errors import ProviderError


class OpenAIProvider(BaseProvider):
    """OpenAI API provider implementation."""

    MODEL_CONTEXT_SIZES = {
        "gpt-4": 8192,
        "gpt-4-32k": 32768,
        "gpt-3.5-turbo": 4096,
        "gpt-3.5-turbo-16k": 16384,
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        organization: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs: Any
    ):
        super().__init__(api_key=api_key, base_url=base_url, **kwargs)
        self.organization = organization
        self.client: Optional[AsyncOpenAI] = None

    def _validate_credentials(self) -> None:
        """Validate OpenAI credentials."""
        if not self.api_key:
            raise ProviderError("OpenAI API key is required")

    async def create_session(self) -> None:
        """Create OpenAI client session."""
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            organization=self.organization,
            base_url=self.base_url,
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            max_retries=self.max_retries,
        )

    async def close_session(self) -> None:
        """Close OpenAI client session."""
        if self.client:
            await self.client.close()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def chat(
        self,
        messages: List[Message],
        model_config: Optional[ModelConfig] = None,
        stream: bool = False,
        **kwargs: Any
    ) -> Union[ProviderResponse, AsyncIterator[ProviderResponse]]:
        """Send a chat request to OpenAI."""
        if not self.client:
            await self.create_session()

        model_config = model_config or ModelConfig(model_name="gpt-3.5-turbo")

        try:
            openai_messages = [
                {
                    "role": msg.role,
                    "content": msg.content,
                    **({"name": msg.name} if msg.name else {}),
                    **({"function_call": msg.function_call.dict()} if msg.function_call else {})
                }
                for msg in messages
            ]

            response = await self.client.chat.completions.create(
                model=model_config.model_name,
                messages=openai_messages,
                max_tokens=model_config.max_tokens,
                temperature=model_config.temperature,
                top_p=model_config.top_p,
                frequency_penalty=model_config.frequency_penalty,
                presence_penalty=model_config.presence_penalty,
                stop=model_config.stop,
                functions=model_config.functions,
                stream=stream,
                **kwargs
            )

            if stream:
                return self._handle_stream_response(response)
            else:
                return self._create_response(response)

        except Exception as e:
            raise ProviderError(f"OpenAI API call failed: {str(e)}")

    async def _handle_stream_response(
        self,
        response: AsyncStream
    ) -> AsyncIterator[ProviderResponse]:
        """Handle streaming response from OpenAI."""
        collected_messages: List[str] = []

        try:
            async for chunk in response:
                if not chunk.choices:
                    continue

                delta = chunk.choices[0].delta
                if not delta.content:
                    continue

                collected_messages.append(delta.content)
                yield ProviderResponse(
                    content=delta.content,
                    raw_response=chunk,
                    usage=UsageInfo(),  # Stream doesn't provide usage info
                    model=chunk.model,
                    provider_name="openai"
                )
        except Exception as e:
            raise ProviderError(f"Error processing stream: {str(e)}")

    def _create_response(self, response: Any) -> ProviderResponse:
        """Create a standardized response from OpenAI response."""
        if not response.choices:
            raise ProviderError("No completion choices returned")

        return ProviderResponse(
            content=response.choices[0].message.content,
            raw_response=response,
            usage=UsageInfo(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
            ),
            finish_reason=response.choices[0].finish_reason,
            model=response.model,
            provider_name="openai"
        )

    async def generate_embedding(
        self,
        text: str,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> List[float]:
        """Generate embeddings using OpenAI."""
        if not self.client:
            await self.create_session()

        try:
            response = await self.client.embeddings.create(
                model=model or "text-embedding-ada-002",
                input=text,
                **kwargs
            )
            return response.data[0].embedding
        except Exception as e:
            raise ProviderError(f"Failed to generate embedding: {str(e)}")

    async def get_token_count(
        self,
        text: str,
        model: Optional[str] = None
    ) -> int:
        """Get token count for text using tiktoken."""
        import tiktoken

        try:
            model = model or "gpt-3.5-turbo"
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception as e:
            raise ProviderError(f"Failed to count tokens: {str(e)}")

    def get_model_context_size(self, model: str) -> int:
        """Get the context size for the given model."""
        return self.MODEL_CONTEXT_SIZES.get(model, 4096)

    async def validate_response(self, response: Any) -> None:
        """Validate OpenAI response."""
        if not response:
            raise ProviderError("Empty response received")
        if not hasattr(response, 'choices'):
            raise ProviderError("Invalid response format")
        if not response.choices:
            raise ProviderError("No completion choices in response")