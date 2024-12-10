import json
from typing import Any, AsyncIterator, Dict, List, Optional, Union
import httpx
from .base import (
    BaseProvider,
    Message,
    ModelConfig,
    ProviderResponse,
    UsageInfo,
)


class OllamaProvider(BaseProvider):
    """Provider class for Ollama API integration."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        timeout: int = 60,
        max_retries: int = 3,
        **kwargs: Any
    ):
        super().__init__(
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            **kwargs
        )

    def _validate_credentials(self) -> None:
        """No API key required for Ollama."""
        pass

    async def create_session(self) -> None:
        """Create an HTTP session for Ollama API calls."""
        self._session = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            **self.kwargs
        )

    async def close_session(self) -> None:
        """Close the HTTP session."""
        if self._session:
            await self._session.aclose()

    def _convert_messages_to_ollama_format(
        self,
        messages: List[Message]
    ) -> List[Dict[str, str]]:
        """Convert messages to Ollama API format."""
        return [
            {
                'role': msg.role,
                'content': msg.content,
                **(({'name': msg.name} if msg.name else {}))
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
        """Send a chat request to Ollama."""
        if not self._session:
            await self.create_session()

        model = model_config.model_name if model_config else kwargs.get('model', 'llama2')

        payload = {
            'model': model,
            'messages': self._convert_messages_to_ollama_format(messages),
            'stream': stream,
            **(model_config.dict(exclude_none=True) if model_config else {}),
            **kwargs
        }

        if stream:
            return self._stream_chat_response(payload)
        else:
            return await self._send_chat_request(payload)

    async def _send_chat_request(self, payload: Dict[str, Any]) -> ProviderResponse:
        """Send a non-streaming chat request."""
        response = await self._session.post('/api/chat', json=payload)
        await self.validate_response(response)

        data = response.json()
        return ProviderResponse(
            content=data['message']['content'],
            raw_response=data,
            usage=UsageInfo(
                prompt_tokens=data.get('prompt_eval_count', 0),
                completion_tokens=data.get('eval_count', 0),
                total_tokens=data.get('total_eval_count', 0)
            ),
            finish_reason=data.get('done', True) and 'stop' or None,
            model=payload['model'],
            provider_name='ollama'
        )

    async def _stream_chat_response(self, payload: Dict[str, Any]) -> AsyncIterator[ProviderResponse]:
        """Handle streaming chat responses."""
        async with self._session.stream('POST', '/api/chat', json=payload) as response:
            await self.validate_response(response)

            async for line in response.aiter_lines():
                if not line:
                    continue

                data = json.loads(line)
                yield ProviderResponse(
                    content=data['message']['content'],
                    raw_response=data,
                    usage=UsageInfo(
                        prompt_tokens=data.get('prompt_eval_count', 0),
                        completion_tokens=data.get('eval_count', 0),
                        total_tokens=data.get('total_eval_count', 0)
                    ),
                    finish_reason='stop' if data.get('done', False) else None,
                    model=payload['model'],
                    provider_name='ollama'
                )

    async def generate_embedding(
        self,
        text: str,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> List[float]:
        """Generate embeddings using Ollama's embed endpoint."""
        if not self._session:
            await self.create_session()

        payload = {
            'model': model or 'llama2',
            'prompt': text,
            **kwargs
        }

        response = await self._session.post('/api/embed', json=payload)
        await self.validate_response(response)

        data = response.json()
        return data['embedding']

    async def get_token_count(self, text: str, model: Optional[str] = None) -> int:
        """Get token count using Ollama's tokenization."""
        # Ollama doesn't provide a direct token counting endpoint
        # This is an approximation
        return len(text.split())

    def get_model_context_size(self, model: str) -> int:
        """Get model's context size."""
        # Default context sizes for known models
        # These should be updated based on actual model specifications
        context_sizes = {
            'llama2': 4096,
            'codellama': 16384,
            'mistral': 8192,
        }
        return context_sizes.get(model.lower(), 4096)

    async def validate_response(self, response: httpx.Response) -> None:
        """Validate Ollama API response."""
        if response.status_code != 200:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            raise Exception(
                f"Ollama API error: {response.status_code} - {error_data.get('error', response.text)}"
            )