from dataclasses import dataclass
from typing import  Literal


@dataclass
class AgentResult:
    """Agent result."""
    type:Literal['text','tool_call','tool_result']
    content:str|None
    tool_arguments:str=""
    tool_name:str=""