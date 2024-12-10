from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class Message(BaseModel):
    """Base message class."""
    content: str
    role: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Conversation(BaseModel):
    """Represents a conversation."""
    id: str
    messages: List[Message] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MemoryItem(BaseModel):
    """Represents a memory item."""
    id: str
    content: str
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
    importance_score: float = 1.0


class BaseMemory(ABC):
    """Base class for memory implementations."""

    @abstractmethod
    async def add_message(self, message: Message) -> None:
        """Add a message to memory."""
        pass

    @abstractmethod
    async def get_messages(
        self,
        limit: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Message]:
        """Retrieve messages from memory."""
        pass

    @abstractmethod
    async def add_memory(self, item: MemoryItem) -> None:
        """Add a memory item."""
        pass

    @abstractmethod
    async def search_memories(
        self,
        query: str,
        limit: int = 5,
        threshold: float = 0.7
    ) -> List[MemoryItem]:
        """Search through memories."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all memories."""
        pass

    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        pass