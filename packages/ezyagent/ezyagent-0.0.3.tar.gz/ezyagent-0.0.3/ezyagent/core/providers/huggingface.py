from typing import Any, AsyncIterator, Dict, List, Optional, Union
from openai import AsyncOpenAI
from .base import (
    BaseProvider,
    Message,
    ModelConfig,
    ProviderResponse,
    UsageInfo,
)


class HuggingFaceProvider(BaseProvider):
    """Provider class for Hugging Face API integration using the OpenAI package."""

    def __init__(
        self,
        api_token: str,
        base_url: Optional[str] = "https://api-inference.huggingface.co/v1/",
        timeout: int = 60,
        max_retries: int = 3,
        **kwargs: Any
    ):
        super().__init__(
            api_key=api_token,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            **kwargs
        )
        self._openai_client: Optional[AsyncOpenAI] = None

    def _validate_credentials(self) -> None:
        """Validate Hugging Face API token."""
        if not self.api_key:
            raise ValueError("Hugging Face API token is required")

    async def create_session(self) -> None:
        """Create OpenAI client session."""
        self._openai_client = AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=self.timeout,
            max_retries=self.max_retries,
            **self.kwargs
        )
        self._session = self._openai_client  # For base provider compatibility

    async def close_session(self) -> None:
        """Close the OpenAI client session."""
        if self._openai_client:
            await self._openai_client.close()

    def _convert_to_hf_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        """Convert internal message format to Hugging Face format."""

        return [
            {
                "role": msg.role,
                "content": msg.content,
                **({"name": msg.name} if msg.name else {})
            } if isinstance(msg,Message) else msg
            for msg in messages
        ]

    async def chat(
        self,
        messages: List[Message],
        model_config: Optional[ModelConfig] = None,
        stream: bool = False,
        **kwargs: Any
    ) -> Union[ProviderResponse, AsyncIterator[ProviderResponse]]:
        """Send a chat request using the Hugging Face API."""
        if not self._openai_client:
            await self.create_session()

        model = model_config.model_name if model_config else kwargs.get("model", "Qwen/Qwen2.5-72B-Instruct")

        # Convert model config to Hugging Face options
        options = {}
        if model_config:
            if model_config.temperature is not None:
                options["temperature"] = model_config.temperature
            if model_config.max_tokens is not None:
                options["max_new_tokens"] = model_config.max_tokens
            if model_config.top_p is not None:
                options["top_p"] = model_config.top_p
            if model_config.frequency_penalty is not None:
                options["frequency_penalty"] = model_config.frequency_penalty
            if model_config.presence_penalty is not None:
                options["presence_penalty"] = model_config.presence_penalty

        gen_args = dict( model=model,
            messages=self._convert_to_hf_messages(messages),
            stream=stream,
            **options)
        print(gen_args)
        response = await self._openai_client.chat.completions.create(**gen_args)

        print(response)


        if stream:
            return self._process_streaming_response(response, model)
        else:
            return self._create_provider_response(response, model)

    async def _process_streaming_response(
        self,
        response: AsyncIterator[Dict[str, Any]],
        model: str
    ) -> AsyncIterator[ProviderResponse]:
        """Process streaming responses from the Hugging Face API."""
        async for chunk in response:
            yield ProviderResponse(
                content=chunk["generated_text"],
                raw_response=chunk,
                usage=UsageInfo(
                    prompt_tokens=0,  # Streaming doesn't provide token counts per chunk
                    completion_tokens=0,
                    total_tokens=0
                ),
                finish_reason="stop" if chunk.get("finished", False) else None,
                model=model,
                provider_name="huggingface"
            )

    def _create_provider_response(self, response: Dict[str, Any], model: str) -> ProviderResponse:
        """Create ProviderResponse from Hugging Face API response."""
        return ProviderResponse(
            content=response["choices"][0]["message"]["content"],
            raw_response=response,
            usage=UsageInfo(
                prompt_tokens=response["usage"]["prompt_tokens"],
                completion_tokens=response["usage"]["completion_tokens"],
                total_tokens=response["usage"]["total_tokens"]
            ),
            finish_reason="stop",
            model=model,
            provider_name="huggingface"
        )

    async def generate_embedding(
        self,
        text: str,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> List[float]:
        """Generate embeddings using the Hugging Face API."""
        if not self._openai_client:
            await self.create_session()

        response = await self._openai_client.embeddings.create(
            model=model or "text-embedding-ada-002",
            input=text,
            **kwargs
        )
        return response["data"][0]["embedding"]

    async def get_token_count(self, text: str, model: Optional[str] = None) -> int:
        """Get token count (approximation since Hugging Face API doesn't provide this)."""
        return len(text.split())

    def get_model_context_size(self, model: str) -> int:
        """Get model's context size."""
        context_sizes = {
            "Qwen/Qwen2.5-72B-Instruct": 8192,
            "Qwen/QwQ-32B-Preview": 8192,
            "Qwen/Qwen2.5-Coder-32B-Instruct": 8192,
            # Add more context size mappings for other models as needed
            "default": 4096
        }
        return context_sizes.get(model.lower(), 4096)

    async def validate_response(self, response: Any) -> None:
        """Validate response (handled by Hugging Face API client)."""
        pass  # The Hugging Face API client already handles response validation