from typing import Optional, Any, Callable, Dict, Literal
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Message class for standardizing communication."""
    role: str
    content: str
    name: Optional[str] = None
    function_call: Any = None

class Tool(BaseModel):
    """Tool definition."""
    name: str
    description: str
    function: Callable
    is_async: bool = True
    parameters: Dict[str, Any] = Field(default_factory=dict)
