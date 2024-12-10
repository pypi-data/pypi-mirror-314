import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from collections import deque

from .base import BaseMemory, Message, MemoryItem, Conversation


class SimpleMemory(BaseMemory):
    """Simple in-memory implementation."""

    def __init__(
        self,
        message_window: Optional[int] = 1000,
        memory_window: Optional[int] = 1000
    ):
        self.conversations: Dict[str, Conversation] = {}
        self.memories: Dict[str, MemoryItem] = {}
        self.message_window = message_window
        self.memory_window = memory_window
        self.current_conversation_id = str(uuid.uuid4())

    async def add_message(self, message: Message) -> None:
        """Add a message to the current conversation."""
        if self.current_conversation_id not in self.conversations:
            self.conversations[self.current_conversation_id] = Conversation(
                id=self.current_conversation_id
            )

        conversation = self.conversations[self.current_conversation_id]
        conversation.messages.append(message)
        conversation.updated_at = datetime.utcnow()

        # Trim messages if window is exceeded
        if self.message_window and len(conversation.messages) > self.message_window:
            conversation.messages = conversation.messages[-self.message_window:]

    async def get_messages(
        self,
        limit: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Message]:
        """Get messages from the current conversation."""
        if self.current_conversation_id not in self.conversations:
            return []

        messages = self.conversations[self.current_conversation_id].messages

        if filters:
            messages = [
                msg for msg in messages
                if all(
                    msg.dict().get(k) == v
                    for k, v in filters.items()
                )
            ]

        if limit:
            messages = messages[-limit:]

        return messages

    async def add_memory(self, item: MemoryItem) -> None:
        """Add a memory item."""
        self.memories[item.id] = item

        # Trim memories if window is exceeded
        if self.memory_window and len(self.memories) > self.memory_window:
            # Remove oldest memories
            sorted_memories = sorted(
                self.memories.items(),
                key=lambda x: x[1].created_at
            )
            self.memories = dict(sorted_memories[-self.memory_window:])

    async def search_memories(
        self,
        query: str,
        limit: int = 5,
        threshold: float = 0.7
    ) -> List[MemoryItem]:
        """Basic semantic search through memories."""
        # In a real implementation, this would use embeddings for semantic search
        # Here we just do simple string matching
        matches = []
        for memory in self.memories.values():
            if query.lower() in memory.content.lower():
                memory.last_accessed = datetime.utcnow()
                matches.append(memory)

        # Sort by importance score and recency
        matches.sort(
            key=lambda x: (x.importance_score, x.last_accessed),
            reverse=True
        )

        return matches[:limit]

    async def clear(self) -> None:
        """Clear all memories and conversations."""
        self.memories.clear()
        self.conversations.clear()
        self.current_conversation_id = str(uuid.uuid4())

    async def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        current_conversation = self.conversations.get(
            self.current_conversation_id,
            Conversation(id=self.current_conversation_id)
        )

        return {
            "total_conversations": len(self.conversations),
            "total_memories": len(self.memories),
            "current_conversation": {
                "id": self.current_conversation_id,
                "message_count": len(current_conversation.messages),
                "created_at": current_conversation.created_at,
                "updated_at": current_conversation.updated_at
            }
        }

    async def new_conversation(self) -> str:
        """Start a new conversation."""
        self.current_conversation_id = str(uuid.uuid4())
        return self.current_conversation_id

    async def summarize_conversation(self) -> str:
        """Generate a summary of the current conversation."""
        if self.current_conversation_id not in self.conversations:
            return "No conversation found."

        conversation = self.conversations[self.current_conversation_id]

        # In a real implementation, this would use an LLM to generate a summary
        # Here we just return basic stats
        return (
            f"Conversation with {len(conversation.messages)} messages, "
            f"started at {conversation.created_at}, "
            f"last updated at {conversation.updated_at}"
        )