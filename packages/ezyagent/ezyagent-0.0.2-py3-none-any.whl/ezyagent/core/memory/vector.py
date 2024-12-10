import numpy as np
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import faiss
from sentence_transformers import SentenceTransformer

from .base import BaseMemory, Message, MemoryItem, Conversation


class VectorMemory(BaseMemory):
    """Vector store-based memory implementation using FAISS."""

    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        dimension: int = 384,
        similarity_threshold: float = 0.7
    ):
        self.conversations: Dict[str, Conversation] = {}
        self.memories: Dict[str, MemoryItem] = {}
        self.current_conversation_id: str = ""

        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)
        self.dimension = dimension
        self.similarity_threshold = similarity_threshold

        # Initialize FAISS index
        self.index = faiss.IndexFlatL2(dimension)
        self.memory_ids: List[str] = []

    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for text."""
        return self.embedding_model.encode(
            text,
            convert_to_tensor=False,
            normalize_embeddings=True
        ).tolist()

    async def add_message(self, message: Message) -> None:
        """Add a message to the current conversation."""
        if not self.current_conversation_id:
            self.current_conversation_id = "default"

        if self.current_conversation_id not in self.conversations:
            self.conversations[self.current_conversation_id] = Conversation(
                id=self.current_conversation_id
            )

        conversation = self.conversations[self.current_conversation_id]
        conversation.messages.append(message)
        conversation.updated_at = datetime.utcnow()

        # Create a memory item from the message
        memory_item = MemoryItem(
            id=str(len(self.memories)),
            content=message.content,
            embedding=self._get_embedding(message.content),
            metadata={
                "role": message.role,
                "conversation_id": self.current_conversation_id,
                **message.metadata
            }
        )
        await self.add_memory(memory_item)

    async def add_memory(self, item: MemoryItem) -> None:
        """Add a memory item to the vector store."""
        if not item.embedding:
            item.embedding = self._get_embedding(item.content)

        # Add to FAISS index
        self.index.add(np.array([item.embedding], dtype=np.float32))
        self.memory_ids.append(item.id)
        self.memories[item.id] = item

    async def search_memories(
        self,
        query: str,
        limit: int = 5,
        threshold: float = None
    ) -> List[MemoryItem]:
        """Search memories using vector similarity."""
        if not self.memory_ids:
            return []

        threshold = threshold or self.similarity_threshold
        query_embedding = self._get_embedding(query)

        # Search FAISS index
        D, I = self.index.search(
            np.array([query_embedding], dtype=np.float32),
            min(limit, len(self.memory_ids))
        )

        results = []
        for distance, idx in zip(D[0], I[0]):
            if idx < len(self.memory_ids):
                memory_id = self.memory_ids[idx]
                memory = self.memories[memory_id]

                # Convert L2 distance to cosine similarity
                similarity = 1 - (distance / 2)
                if similarity >= threshold:
                    memory.last_accessed = datetime.utcnow()
                    results.append(memory)

        return results

    async def get_messages(
        self,
        limit: Optional[int] = None,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Message]:
        """Get messages from the current conversation."""
        if not self.current_conversation_id:
            return []

        conversation = self.conversations.get(self.current_conversation_id)
        if not conversation:
            return []

        messages = conversation.messages

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

    async def clear(self) -> None:
        """Clear all memories and reset the index."""
        self.conversations.clear()
        self.memories.clear()
        self.memory_ids.clear()
        self.current_conversation_id = ""
        self.index = faiss.IndexFlatL2(self.dimension)

    async def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        return {
            "total_conversations": len(self.conversations),
            "total_memories": len(self.memories),
            "current_conversation_id": self.current_conversation_id,
            "embedding_model": self.embedding_model.get_sentence_embedding_dimension(),
            "index_size": self.index.ntotal
        }