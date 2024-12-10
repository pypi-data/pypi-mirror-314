import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Union
from pydantic import BaseModel, create_model

from .base import BaseTool, FunctionTool, ModelTool, ToolMetadata, ToolParameter, ToolParameterType


def create_tool_from_function(
    func: Callable,
    name: Optional[str] = None,
    description: Optional[str] = None,
    **kwargs: Any
) -> FunctionTool:
    """Create a tool from a function."""
    return FunctionTool(
        func=func,
        name=name,
        description=description,
        **kwargs
    )


def create_tool_from_model(
    model: Type[BaseModel],
    execute_func: Callable,
    name: Optional[str] = None,
    description: Optional[str] = None,
    **kwargs: Any
) -> ModelTool:
    """Create a tool from a Pydantic model."""
    return ModelTool(
        model=model,
        execute_func=execute_func,
        name=name,
        description=description,
        **kwargs
    )


def create_tool_model(
    name: str,
    parameters: Dict[str, tuple[Type, Any]],
    description: Optional[str] = None
) -> Type[BaseModel]:
    """Create a Pydantic model for tool parameters."""
    return create_model(
        name,
        **parameters,
        __doc__=description
    )


def infer_parameter_type(annotation: Any) -> ToolParameterType:
    """Infer ToolParameterType from Python type annotation."""
    if annotation == str:
        return ToolParameterType.STRING
    elif annotation == int:
        return ToolParameterType.INTEGER
    elif annotation == float:
        return ToolParameterType.NUMBER
    elif annotation == bool:
        return ToolParameterType.BOOLEAN
    elif annotation == list or getattr(annotation, "__origin__", None) == list:
        return ToolParameterType.ARRAY
    elif annotation == dict or getattr(annotation, "__origin__", None) == dict:
        return ToolParameterType.OBJECT
    else:
        return ToolParameterType.STRING


def validate_tool_definition(tool: BaseTool) -> List[str]:
    """Validate tool definition and return list of warnings."""
    warnings = []

    # Check metadata
    if not tool.metadata.description:
        warnings.append("Tool is missing a description")

    # Check parameters
    for param in tool.metadata.parameters:
        if not param.description:
            warnings.append(f"Parameter '{param.name}' is missing a description")

    # Check execution function
    if isinstance(tool, FunctionTool):
        sig = inspect.signature(tool.func)
        param_names = {p.name for p in tool.metadata.parameters}
        func_params = set(sig.parameters.keys()) - {"self", "cls"}

        if param_names != func_params:
            warnings.append(
                f"Parameter mismatch between metadata and function: "
                f"metadata={param_names}, function={func_params}"
            )

    return warnings


class ToolDecorator:
    """Decorator utility for creating tools."""

    @staticmethod
    def tool(
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs: Any
    ) -> Callable:
        """Decorator to create a tool from a function."""

        def decorator(func: Callable) -> FunctionTool:
            return create_tool_from_function(
                func=func,
                name=name or func.__name__,
                description=description or func.__doc__,
                **kwargs
            )

        return decorator

    @staticmethod
    def model_tool(
        model: Type[BaseModel],
        name: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs: Any
    ) -> Callable:
        """Decorator to create a tool from a Pydantic model."""

        def decorator(func: Callable) -> ModelTool:
            return create_tool_from_model(
                model=model,
                execute_func=func,
                name=name or func.__name__,
                description=description or func.__doc__,
                **kwargs
            )

        return decorator


# Example usage of the decorator
tool = ToolDecorator.tool
model_tool = ToolDecorator.model_tool