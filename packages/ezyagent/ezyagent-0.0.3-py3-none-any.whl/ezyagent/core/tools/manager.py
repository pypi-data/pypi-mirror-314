from typing import Any, Dict, List, Optional, Type, Union
from pydantic import ValidationError
from .base import BaseTool, ToolException, ToolExecutionError


class ToolManager:
    """Manages tool registration and execution."""

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._execution_history: List[Dict[str, Any]] = []

    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        record_history: bool = True
    ) -> Any:
        """Execute a tool with given parameters."""
        if tool_name not in self.tools:
            raise ToolException(f"Tool {tool_name} not found")

        tool = self.tools[tool_name]
        execution_record = {
            "tool_name": tool_name,
            "parameters": parameters,
            "timestamp": self._get_timestamp(),
            "status": "pending"
        }

        try:
            result = await tool.execute(**parameters)
            execution_record.update({
                "status": "success",
                "result": result
            })
            return result
        except Exception as e:
            execution_record.update({
                "status": "error",
                "error": str(e)
            })
            raise ToolExecutionError(f"Tool execution failed: {str(e)}")
        finally:
            if record_history:
                self._execution_history.append(execution_record)

    def get_tools_schema(self) -> List[Dict[str, Any]]:
        """Get JSON schema for all registered tools."""
        return [tool.to_dict() for tool in self.tools.values()]

    def get_execution_history(
        self,
        tool_name: Optional[str] = None,
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Get tool execution history with optional filters."""
        history = self._execution_history

        if tool_name:
            history = [h for h in history if h["tool_name"] == tool_name]
        if status:
            history = [h for h in history if h["status"] == status]
        if limit:
            history = history[-limit:]

        return history

    def clear_history(self) -> None:
        """Clear execution history."""
        self._execution_history = []

    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return list(self.tools.keys())

    def get_tool_metadata(self, tool_name: str) -> Dict[str, Any]:
        """Get metadata for a specific tool."""
        if tool_name not in self.tools:
            raise ToolException(f"Tool {tool_name} not found")
        return self.tools[tool_name].metadata.dict()

    def validate_parameters(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> bool:
        """Validate parameters for a tool."""
        if tool_name not in self.tools:
            raise ToolException(f"Tool {tool_name} not found")

        tool = self.tools[tool_name]
        try:
            # If it's a ModelTool, use the model for validation
            if hasattr(tool, 'model'):
                tool.model(**parameters)
            return True
        except ValidationError as e:
            raise ToolException(f"Invalid parameters: {str(e)}")

    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.utcnow().isoformat()