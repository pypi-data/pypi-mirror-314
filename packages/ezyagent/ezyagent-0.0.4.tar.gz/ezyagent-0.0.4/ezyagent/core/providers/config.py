from dataclasses import dataclass
from typing import Optional

@dataclass
class ProviderConfig:
    """Configuration for LLM provider"""
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    model: str = ""
    provider: Optional[str] = None