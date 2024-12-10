import aiohttp
import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from .base import ModelTool, ToolMetadata, ToolParameter, ToolParameterType


class SearchParams(BaseModel):
    """Parameters for web search."""
    query: str
    num_results: Optional[int] = 5

    class Config:
        schema_extra = {
            "description": "Parameters for performing a web search"
        }


class WebSearchTool(ModelTool):
    """Tool for performing web searches."""

    def __init__(self, api_key: str, **kwargs: Any):
        super().__init__(
            model=SearchParams,
            execute_func=self._search,
            name="web_search",
            description="Search the web for information",
            **kwargs
        )
        self.api_key = api_key
        self._session: Optional[aiohttp.ClientSession] = None

    async def _search(self, params: SearchParams) -> List[Dict[str, str]]:
        """Perform web search."""
        if not self._session:
            self._session = aiohttp.ClientSession()

        try:
            # Example using SerpAPI - replace with your preferred search API
            url = "https://serpapi.com/search"
            params_dict = {
                "q": params.query,
                "num": params.num_results,
                "api_key": self.api_key,
                "engine": "google",
            }

            async with self._session.get(url, params=params_dict) as response:
                data = await response.json()

                results = []
                for item in data.get("organic_results", [])[:params.num_results]:
                    results.append({
                        "title": item.get("title", ""),
                        "snippet": item.get("snippet", ""),
                        "link": item.get("link", ""),
                    })

                return results

        except Exception as e:
            raise Exception(f"Search failed: {str(e)}")


class Calculator(ModelTool):
    """Tool for performing mathematical calculations."""

    class CalculationParams(BaseModel):
        expression: str

        class Config:
            schema_extra = {
                "description": "Parameters for mathematical calculation"
            }

    def __init__(self, **kwargs: Any):
        super().__init__(
            model=self.CalculationParams,
            execute_func=self._calculate,
            name="calculator",
            description="Perform mathematical calculations",
            **kwargs
        )

    async def _calculate(self, params: CalculationParams) -> float:
        """Perform calculation."""
        try:
            # Note: This is a simple example. In production, you'd want to use
            # a safer evaluation method
            import math
            allowed_names = {
                k: v for k, v in math.__dict__.items()
                if not k.startswith('__')
            }
            allowed_names.update({
                'abs': abs,
                'float': float,
                'int': int,
                'max': max,
                'min': min,
                'pow': pow,
                'round': round,
            })

            code = compile(params.expression, '<string>', 'eval')
            for name in code.co_names:
                if name not in allowed_names:
                    raise NameError(f"Use of {name} not allowed")

            return eval(code, {"__builtins__": {}}, allowed_names)

        except Exception as e:
            raise Exception(f"Calculation failed: {str(e)}")


class WeatherTool(ModelTool):
    """Tool for getting weather information."""

    class WeatherParams(BaseModel):
        location: str
        units: Optional[str] = "metric"

        class Config:
            schema_extra = {
                "description": "Parameters for weather lookup"
            }

    def __init__(self, api_key: str, **kwargs: Any):
        super().__init__(
            model=self.WeatherParams,
            execute_func=self._get_weather,
            name="weather",
            description="Get current weather information for a location",
            **kwargs
        )
        self.api_key = api_key
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_weather(self, params: WeatherParams) -> Dict[str, Any]:
        """Get weather information."""
        if not self._session:
            self._session = aiohttp.ClientSession()

        try:
            # Using OpenWeatherMap API
            url = "https://api.openweathermap.org/data/2.5/weather"
            params_dict = {
                "q": params.location,
                "units": params.units,
                "appid": self.api_key,
            }

            async with self._session.get(url, params=params_dict) as response:
                data = await response.json()

                if response.status != 200:
                    raise Exception(data.get("message", "Weather lookup failed"))

                return {
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                }

        except Exception as e:
            raise Exception(f"Weather lookup failed: {str(e)}")