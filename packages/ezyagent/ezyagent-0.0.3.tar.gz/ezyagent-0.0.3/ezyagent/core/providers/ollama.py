from typing import Any, AsyncIterator, Dict, List, Optional, Union
from ollama import AsyncClient
from .base import (
    BaseProvider,
    Message,
    ModelConfig,
    ProviderResponse,
    UsageInfo,
)


class OllamaProvider(BaseProvider):
    """Provider class for Ollama API integration using official client."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        timeout: int = 60,
        max_retries: int = 3,
        **kwargs: Any
    ):
        super().__init__(
            api_key=None,  # Ollama doesn't require API key
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            **kwargs
        )
        self._ollama_client: Optional[AsyncClient] = None

    def _validate_credentials(self) -> None:
        """No API key required for Ollama."""
        pass

    async def create_session(self) -> None:
        """Create Ollama AsyncClient."""
        self._ollama_client = AsyncClient(
            host=self.base_url,
            timeout=self.timeout,
            **self.kwargs
        )
        self._session = self._ollama_client._client  # For compatibility with base provider

    async def close_session(self) -> None:
        """Close the Ollama client session."""
        if self._ollama_client:
            await self._ollama_client._client.aclose()

    def _convert_to_ollama_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        """Convert internal message format to Ollama format."""
        return [
            {
                "role": msg.role,
                "content": msg.content,
                **({"name": msg.name} if msg.name else {})
            }
            for msg in messages
        ]

    async def chat(
        self,
        messages: List[Message],
        model_config: Optional[ModelConfig] = None,
        stream: bool = False,
        **kwargs: Any
    ) -> Union[ProviderResponse, AsyncIterator[ProviderResponse]]:
        """Send a chat request using Ollama client."""
        if not self._ollama_client:
            await self.create_session()

        model = model_config.model_name if model_config else kwargs.get("model", "llama2")

        # Convert model config to Ollama options
        options = {}
        if model_config:
            if model_config.temperature is not None:
                options["temperature"] = model_config.temperature
            if model_config.top_p is not None:
                options["top_p"] = model_config.top_p
            if model_config.frequency_penalty is not None:
                options["frequency_penalty"] = model_config.frequency_penalty
            if model_config.presence_penalty is not None:
                options["presence_penalty"] = model_config.presence_penalty
            if model_config.max_tokens is not None:
                options["num_predict"] = model_config.max_tokens

        response = await self._ollama_client.chat(
            model=model,
            messages=self._convert_to_ollama_messages(messages),
            stream=stream,
            options=options,
            **kwargs
        )

        if stream:
            return self._process_streaming_response(response, model)
        else:
            return self._create_provider_response(response, model)

    async def _process_streaming_response(
        self,
        response: AsyncIterator[Dict[str, Any]],
        model: str
    ) -> AsyncIterator[ProviderResponse]:
        """Process streaming responses from Ollama."""
        async for chunk in response:
            yield ProviderResponse(
                content=chunk["message"]["content"],
                raw_response=chunk,
                usage=UsageInfo(
                    prompt_tokens=chunk.get("prompt_eval_count", 0),
                    completion_tokens=chunk.get("eval_count", 0),
                    total_tokens=chunk.get("total_eval_count", 0)
                ),
                finish_reason="stop" if chunk.get("done", False) else None,
                model=model,
                provider_name="ollama"
            )

    def _create_provider_response(self, response: Dict[str, Any], model: str) -> ProviderResponse:
        """Create ProviderResponse from Ollama response."""
        return ProviderResponse(
            content=response["message"]["content"],
            raw_response=response,
            usage=UsageInfo(
                prompt_tokens=response.get("prompt_eval_count", 0),
                completion_tokens=response.get("eval_count", 0),
                total_tokens=response.get("total_eval_count", 0)
            ),
            finish_reason="stop" if response.get("done", True) else None,
            model=model,
            provider_name="ollama"
        )

    async def generate_embedding(
        self,
        text: str,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> List[float]:
        """Generate embeddings using Ollama client."""
        if not self._ollama_client:
            await self.create_session()

        response = await self._ollama_client.embed(
            model=model or "llama2",
            input=text,
            **kwargs
        )
        return response["embedding"]

    async def get_token_count(self, text: str, model: Optional[str] = None) -> int:
        """Get token count (approximation since Ollama doesn't provide this)."""
        return len(text.split())

    def get_model_context_size(self, model: str) -> int:
        """Get model's context size."""
        context_sizes = {
            "llama2": 4096,
            "codellama": 16384,
            "mistral": 8192,
            "mixtral": 32768,
            "phi": 2048,
            "neural-chat": 8192,
            "gemma": 8192
        }
        return context_sizes.get(model.lower(), 4096)

    async def validate_response(self, response: Any) -> None:
        """Validate response (handled by Ollama client)."""
        pass  # The Ollama client already handles response validation