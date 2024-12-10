import asyncio
from typing import Any, AsyncIterator, Callable, Dict, List, Optional, Union, Iterable, Sequence
from langchain_core.utils.function_calling import convert_to_openai_tool
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam
from openai import NotGiven, NOT_GIVEN
from .base import BaseAgent
from .models import Tool
from .schemas import AgentResult
from .models import Message

class PersonAgent:
    def __init__(self, system_prompt, chat):
        self.system_prompt = system_prompt
        self.chat = chat

    def __call__(self,messages, model=None,*args, **kwargs):
        _sys_prompt = kwargs.pop('system_prompt',None) or self.system_prompt
        if isinstance(messages,str):
            messages = [Message(role='system',content=_sys_prompt),
                        Message(role='user', content=messages)]
        return self.chat(messages=messages,
                         model= model,
                         *args, **kwargs)


class Agent(BaseAgent):
    """Agent class with tool support."""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._tool_choice: Optional[str] = None
        self._temp_tools: Dict[str, Tool] = {}

    def __call__(self,system_prompt):
        return PersonAgent(system_prompt=system_prompt,
                           chat=self.chat)



    def _convert_tools_to_openai_format(self, tools: Optional[Sequence[Callable]] = None) -> List[Dict[str, Any]]:
        """Convert all tools to OpenAI format."""
        openai_tools = []

        # Add registered tools
        for tool in self.tools.values():
            openai_tools.append(convert_to_openai_tool(tool.function))

        # Add temporary tools
        if tools:
            for func in tools:
                openai_tools.append(convert_to_openai_tool(func))
                # Store in temporary tools for future reference if needed
                tool = Tool(
                    name=func.__name__,
                    description=func.__doc__ or "No description provided",
                    function=func,
                    is_async=asyncio.iscoroutinefunction(func)
                )
                self._temp_tools[tool.name] = tool

        return openai_tools

    async def chat(
        self,
        messages: Union[Iterable[ChatCompletionMessageParam], str],
        tool_choice: Optional[str] = None,
        extra_tools: Optional[Sequence[Callable]] = None,
        tools: Optional[Iterable[ChatCompletionToolParam]] | NotGiven = NOT_GIVEN,
        *args: Any,
        **kwargs: Any
    ) -> Union[AgentResult, AsyncIterator[AgentResult]]:
        """Enhanced async chat method with tool support."""
        self.return_tool_arguments: bool =kwargs.pop('return_tool_arguments',False)

        try:
            # Clear temporary tools from previous chat
            self._temp_tools.clear()

            # Convert tools if any are provided
            if self.tools or extra_tools:
                chat_tools = self._convert_tools_to_openai_format(extra_tools)
                # If tools were explicitly passed, append them to our converted tools
                if isinstance(tools, Iterable):
                    chat_tools.extend(tools)
                kwargs['tools'] = chat_tools

                # Handle tool choice
                choice = tool_choice or self._tool_choice
                if choice is not None:
                    if choice in ("auto", "none"):
                        kwargs['tool_choice'] = choice
                    else:
                        kwargs['tool_choice'] = {
                            "type": "function",
                            "function": {"name": choice}
                        }
            elif isinstance(tools, Iterable):
                # If only explicit tools were passed
                kwargs['tools'] = tools

            # Call parent chat method with modified kwargs
            return await super().chat(messages, *args, **kwargs)

        finally:
            # Clear temporary tools after chat completion
            self._temp_tools.clear()

    def print_agent_info(self) -> None:
        """Extended print_agent_info to include temporary tools."""
        super().print_agent_info()

        # Print temporary tools if any exist
        if self._temp_tools:
            from tabulate import tabulate

            temp_tools_data = []
            for name, tool in self._temp_tools.items():
                temp_tools_data.append([
                    "Name", name,
                ])
                temp_tools_data.append([
                    "Description", tool.description
                ])
                temp_tools_data.append([
                    "Is Async", str(tool.is_async)
                ])
                temp_tools_data.append(["-" * 20, "-" * 40])

            print("\nTEMPORARY TOOLS")
            print(tabulate(temp_tools_data, tablefmt="grid"))