class AgentError(Exception):
    """Base class for all agent errors."""

    def __init__(
        self,
        message: str,
        *args: object,
        provider_error: Exception | None = None,
        context: dict | None = None
    ) -> None:
        super().__init__(message, *args)
        self.provider_error = provider_error
        self.context = context or {}


class ProviderError(AgentError):
    """Error from the LLM provider."""
    pass


class ToolError(AgentError):
    """Error while executing a tool."""
    pass


class ValidationError(AgentError):
    """Error during input validation."""
    pass


class ConfigurationError(AgentError):
    """Error in agent configuration."""
    pass