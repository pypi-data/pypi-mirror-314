from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, Union
from pydantic import BaseModel, Field, create_model


class ToolException(Exception):
    """Base exception for tool-related errors."""
    pass


class ToolExecutionError(ToolException):
    """Raised when tool execution fails."""
    pass


class ToolValidationError(ToolException):
    """Raised when tool validation fails."""
    pass


class ToolParameterType(str, Enum):
    """Supported parameter types for tools."""
    STRING = "string"
    INTEGER = "integer"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"


class ToolParameter(BaseModel):
    """Definition of a tool parameter."""
    name: str
    type: ToolParameterType
    description: str
    required: bool = True
    default: Optional[Any] = None
    enum: Optional[List[Any]] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    pattern: Optional[str] = None


class ToolMetadata(BaseModel):
    """Metadata for a tool."""
    name: str
    description: str
    parameters: List[ToolParameter] = Field(default_factory=list)
    version: str = "1.0.0"
    author: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    requires_auth: bool = False
    is_async: bool = True


class BaseTool(ABC):
    """Base class for all tools."""

    def __init__(
        self,
        metadata: Optional[ToolMetadata] = None,
        **kwargs: Any
    ):
        self.metadata = metadata or self._generate_metadata()
        self._validate_metadata()
        self.kwargs = kwargs

    @abstractmethod
    def _generate_metadata(self) -> ToolMetadata:
        """Generate tool metadata from class attributes and docstring."""
        pass

    def _validate_metadata(self) -> None:
        """Validate tool metadata."""
        if not self.metadata.name:
            raise ToolValidationError("Tool name is required")
        if not self.metadata.description:
            raise ToolValidationError("Tool description is required")

    @abstractmethod
    async def execute(
        self,
        **kwargs: Any
    ) -> Any:
        """Execute the tool."""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert tool to dictionary format for LLM function calling."""
        return {
            "name": self.metadata.name,
            "description": self.metadata.description,
            "parameters": {
                "type": "object",
                "properties": {
                    param.name: {
                        "type": param.type.value,
                        "description": param.description,
                        **({"enum": param.enum} if param.enum else {}),
                        **({"minimum": param.min_value} if param.min_value is not None else {}),
                        **({"maximum": param.max_value} if param.max_value is not None else {}),
                        **({"pattern": param.pattern} if param.pattern else {}),
                    }
                    for param in self.metadata.parameters
                },
                "required": [
                    param.name for param in self.metadata.parameters
                    if param.required
                ]
            }
        }


class FunctionTool(BaseTool):
    """Tool created from a function."""

    def __init__(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs: Any
    ):
        self.func = func
        self._name = name or func.__name__
        self._description = description or func.__doc__ or ""
        super().__init__(**kwargs)

    def _generate_metadata(self) -> ToolMetadata:
        """Generate metadata from function signature."""
        from inspect import signature, Parameter
        import docstring_parser

        sig = signature(self.func)
        doc = docstring_parser.parse(self.func.__doc__ or "")

        parameters: List[ToolParameter] = []

        for name, param in sig.parameters.items():
            # Skip self/cls for methods
            if name in ("self", "cls"):
                continue

            param_doc = next(
                (p for p in doc.params if p.arg_name == name),
                None
            )

            param_type = self._get_parameter_type(param.annotation)

            parameters.append(
                ToolParameter(
                    name=name,
                    type=param_type,
                    description=param_doc.description if param_doc else "",
                    required=param.default == Parameter.empty,
                    default=param.default if param.default != Parameter.empty else None,
                )
            )

        return ToolMetadata(
            name=self._name,
            description=self._description,
            parameters=parameters,
            is_async=self._is_async_function(self.func)
        )

    def _get_parameter_type(
        self,
        annotation: Any
    ) -> ToolParameterType:
        """Convert Python type annotation to ToolParameterType."""
        if annotation == str:
            return ToolParameterType.STRING
        elif annotation == int:
            return ToolParameterType.INTEGER
        elif annotation == float:
            return ToolParameterType.NUMBER
        elif annotation == bool:
            return ToolParameterType.BOOLEAN
        elif annotation == list:
            return ToolParameterType.ARRAY
        elif annotation == dict:
            return ToolParameterType.OBJECT
        else:
            return ToolParameterType.STRING

    def _is_async_function(self, func: Callable) -> bool:
        """Check if function is async."""
        import inspect
        return inspect.iscoroutinefunction(func)

    async def execute(self, **kwargs: Any) -> Any:
        """Execute the function."""
        try:
            if self._is_async_function(self.func):
                return await self.func(**kwargs)
            else:
                return self.func(**kwargs)
        except Exception as e:
            raise ToolExecutionError(f"Tool execution failed: {str(e)}")


class ModelTool(BaseTool):
    """Tool created from a Pydantic model."""

    def __init__(
        self,
        model: Type[BaseModel],
        execute_func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs: Any
    ):
        self.model = model
        self.execute_func = execute_func
        self._name = name or model.__name__
        self._description = description or model.__doc__ or ""
        super().__init__(**kwargs)

    def _generate_metadata(self) -> ToolMetadata:
        """Generate metadata from Pydantic model."""
        schema = self.model.model_json_schema()

        parameters: List[ToolParameter] = []

        for name, field in schema.get("properties", {}).items():
            parameters.append(
                ToolParameter(
                    name=name,
                    type=ToolParameterType(field.get("type", "string")),
                    description=field.get("description", ""),
                    required=name in schema.get("required", []),
                    enum=field.get("enum"),
                    min_value=field.get("minimum"),
                    max_value=field.get("maximum"),
                    pattern=field.get("pattern"),
                )
            )

        return ToolMetadata(
            name=self._name,
            description=self._description,
            parameters=parameters,
            is_async=self._is_async_function(self.execute_func)
        )

    async def execute(self, **kwargs: Any) -> Any:
        """Execute the tool with model validation."""
        try:
            # Validate input against model
            validated_data = self.model(**kwargs)

            # Execute function with validated data
            if self._is_async_function(self.execute_func):
                return await self.execute_func(validated_data)
            else:
                return self.execute_func(validated_data)

        except Exception as e:
            raise ToolExecutionError(f"Tool execution failed: {str(e)}")

    def _is_async_function(self, func: Callable) -> bool:
        """Check if function is async."""
        import inspect
        return inspect.iscoroutinefunction(func)