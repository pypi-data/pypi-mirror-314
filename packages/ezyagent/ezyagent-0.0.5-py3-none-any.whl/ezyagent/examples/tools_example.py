import asyncio
from typing import Optional
from pydantic import BaseModel

from ezyagent.core.tools import (
    ToolManager,
    tool,
    model_tool,
    WeatherTool,
    Calculator,
)


# Example 1: Function-based tool
@tool(name="greet")
async def greet(name: str, language: str = "en") -> str:
    """Greet someone in different languages.

    Args:
        name: Name of the person to greet
        language: Language code (en, es, fr)
    """
    greetings = {
        "en": "Hello",
        "es": "Hola",
        "fr": "Bonjour"
    }
    return f"{greetings.get(language, 'Hello')} {name}!"


# Example 2: Model-based tool
class SearchQuery(BaseModel):
    """Search query parameters."""
    query: str
    max_results: Optional[int] = 5


@model_tool(model=SearchQuery, name="search")
async def search(params: SearchQuery) -> list[str]:
    """Search for information.

    Args:
        params: Search parameters
    """
    # Simulate search
    return [
        f"Result {i} for: {params.query}"
        for i in range(params.max_results)
    ]


async def main():
    # Create tool manager
    manager = ToolManager()

    # Register tools
    manager.register(greet)
    manager.register(search)
    manager.register(Calculator())
    manager.register(WeatherTool(api_key="your-api-key"))

    # Execute tools
    try:
        # Example 1: Simple greeting
        result = await manager.execute_tool(
            "greet",
            {"name": "Alice", "language": "es"}
        )
        print(f"Greeting result: {result}")

        # Example 2: Search with model
        result = await manager.execute_tool(
            "search",
            {"query": "AI agents", "max_results": 3}
        )
        print(f"Search results: {result}")

        # Example 3: Calculator
        result = await manager.execute_tool(
            "calculator",
            {"expression": "2 * (3 + 4)"}
        )
        print(f"Calculation result: {result}")

        # Show execution history
        print("\nExecution history:")
        for record in manager.get_execution_history():
            print(f"- {record['tool_name']}: {record['status']}")

        # Show available tools
        print("\nAvailable tools:")
        for tool_name in manager.get_available_tools():
            metadata = manager.get_tool_metadata(tool_name)
            print(f"- {tool_name}: {metadata['description']}")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())