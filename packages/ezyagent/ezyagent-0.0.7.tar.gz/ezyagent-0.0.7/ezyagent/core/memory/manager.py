from datetime import datetime
from typing import Any, Dict, List, Optional, Type, Union
from .base import BaseMemory, Message, MemoryItem
from .simple import SimpleMemory

class MemoryManager:
    """Manages different types of memory implementations."""

    def __init__(
        self,
        memory_type: str = "simple",
        **kwargs: Any
    ):
        self.memory: BaseMemory = self._create_memory(memory_type, **kwargs)

    def _create_memory(
        self,
        memory_type: str,
        **kwargs: Any
    ) -> BaseMemory:
        """Create memory instance based on type."""
        if memory_type == "simple":
            return SimpleMemory(**kwargs)
        elif memory_type == "vector":
            return VectorMemory(**kwargs)
        else:
            raise ValueError(f"Unknown memory type: {memory_type}")

    async def add_message(self, content: str, role: str, **metadata: Any) -> None:
        """Add a message to memory."""
        message = Message(
            content=content,
            role=role,
            metadata=metadata
        )
        await self.memory.add_message(message)

    async def add_memory(
        self,
        content: str,
        importance: float = 1.0,
        **metadata: Any
    ) -> None:
        """Add a memory item."""
        memory_item = MemoryItem(
            id=str(id(content)),
            content=content,
            importance_score=importance,
            metadata=metadata
        )
        await self.memory.add_memory(memory_item)

    async def search(
        self,
        query: str,
        limit: int = 5,
        threshold: float = 0.7
    ) -> List[MemoryItem]:
        """Search through memories."""
        return await self.memory.search_memories(
            query,
            limit=limit,
            threshold=threshold
        )

    async def get_recent_messages(
        self,
        limit: Optional[int] = None,
        role: Optional[str] = None
    ) -> List[Message]:
        """Get recent messages."""
        filters = {"role": role} if role else None
        return await self.memory.get_messages(
            limit=limit,
            filters=filters
        )

    async def get_conversation_summary(
        self,
        summarize_with_llm: bool = False,
        llm: Optional[Any] = None
    ) -> str:
        """Get a summary of the current conversation."""
        messages = await self.memory.get_messages()

        if not messages:
            return "No conversation history."

        if summarize_with_llm and llm:
            # Use LLM to generate summary
            conversation = "\n".join(
                f"{msg.role}: {msg.content}" for msg in messages
            )
            prompt = f"Summarize this conversation:\n{conversation}"
            summary = await llm.chat([{"role": "user", "content": prompt}])
            return summary
        else:
            # Simple statistical summary
            role_counts = {}
            for message in messages:
                role_counts[message.role] = role_counts.get(message.role, 0) + 1

            summary = [
                f"Conversation with {len(messages)} messages:",
                "Participants:"
            ]
            for role, count in role_counts.items():
                summary.append(f"- {role}: {count} messages")

            return "\n".join(summary)

    async def clear_memory(self, memory_type: Optional[str] = None) -> None:
        """Clear specific or all types of memory."""
        await self.memory.clear()

    async def export_memories(
        self,
        format: str = "json",
        include_embeddings: bool = False
    ) -> Union[str, Dict[str, Any]]:
        """Export memories in specified format."""
        memories = self.memory.memories

        if format == "json":
            import json
            export_data = {
                "messages": [
                    msg.dict(exclude_none=True)
                    for msg in await self.memory.get_messages()
                ],
                "memories": [
                    memory.dict(
                        exclude={"embedding"} if not include_embeddings else set()
                    )
                    for memory in memories.values()
                ],
                "stats": await self.memory.get_stats()
            }
            return json.dumps(export_data, default=str, indent=2)

        elif format == "dict":
            return {
                "messages": [
                    msg.dict(exclude_none=True)
                    for msg in await self.memory.get_messages()
                ],
                "memories": [
                    memory.dict(
                        exclude={"embedding"} if not include_embeddings else set()
                    )
                    for memory in memories.values()
                ],
                "stats": await self.memory.get_stats()
            }
        else:
            raise ValueError(f"Unsupported export format: {format}")

    async def import_memories(
        self,
        data: Union[str, Dict[str, Any]],
        clear_existing: bool = False
    ) -> None:
        """Import memories from exported data."""
        if clear_existing:
            await self.clear_memory()

        if isinstance(data, str):
            import json
            data = json.loads(data)

        # Import messages
        for msg_data in data.get("messages", []):
            message = Message(**msg_data)
            await self.memory.add_message(message)

        # Import memories
        for mem_data in data.get("memories", []):
            memory = MemoryItem(**mem_data)
            await self.memory.add_memory(memory)

    async def merge_memories(
        self,
        other_memory: BaseMemory,
        strategy: str = "append"
    ) -> None:
        """Merge another memory instance into this one."""
        if strategy == "append":
            # Simply append all messages and memories
            messages = await other_memory.get_messages()
            for message in messages:
                await self.memory.add_message(message)

            for memory in other_memory.memories.values():
                await self.memory.add_memory(memory)

        elif strategy == "interleave":
            # Interleave messages based on timestamp
            current_messages = await self.memory.get_messages()
            other_messages = await other_memory.get_messages()

            all_messages = sorted(
                current_messages + other_messages,
                key=lambda x: x.created_at
            )

            await self.clear_memory()
            for message in all_messages:
                await self.memory.add_message(message)
        else:
            raise ValueError(f"Unsupported merge strategy: {strategy}")

    async def get_memory_window(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Message]:
        """Get messages within a specific time window."""
        messages = await self.memory.get_messages()

        filtered_messages = []
        for message in messages:
            if start_time and message.created_at < start_time:
                continue
            if end_time and message.created_at > end_time:
                continue
            filtered_messages.append(message)

        if limit:
            filtered_messages = filtered_messages[-limit:]

        return filtered_messages

    async def maintain_memory(
        self,
        max_size: Optional[int] = None,
        min_importance: Optional[float] = None
    ) -> None:
        """Maintain memory by removing old or unimportant items."""
        if max_size is not None:
            memories = list(self.memory.memories.values())
            if len(memories) > max_size:
                # Sort by importance and recency
                memories.sort(
                    key=lambda x: (x.importance_score, x.last_accessed),
                    reverse=True
                )
                # Keep only the most important/recent memories
                keep_memories = memories[:max_size]
                self.memory.memories = {
                    mem.id: mem for mem in keep_memories
                }

        if min_importance is not None:
            self.memory.memories = {
                k: v for k, v in self.memory.memories.items()
                if v.importance_score >= min_importance
            }