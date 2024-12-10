import asyncio
from datetime import datetime, timedelta
from ezyagent.core.memory import MemoryManager


async def main():
    # Create memory manager with vector store
    manager = MemoryManager(
        memory_type="vector",
        embedding_model="all-MiniLM-L6-v2"
    )

    # Add some messages
    await manager.add_message(
        "Hello, how can I help you?",
        role="assistant"
    )
    await manager.add_message(
        "I need help with Python programming.",
        role="user"
    )
    await manager.add_message(
        "What specific aspects of Python do you need help with?",
        role="assistant"
    )

    # Add some memories
    await manager.add_memory(
        "User is interested in Python programming",
        importance=0.8,
        topic="programming",
        skills=["python"]
    )
    await manager.add_memory(
        "User is a beginner programmer",
        importance=0.9,
        topic="skill_level"
    )

    # Search memories
    print("\nSearching memories about Python:")
    memories = await manager.search("python programming")
    for memory in memories:
        print(f"- {memory.content} (importance: {memory.importance_score})")

    # Get recent messages
    print("\nRecent messages:")
    messages = await manager.get_recent_messages(limit=5)
    for msg in messages:
        print(f"{msg.role}: {msg.content}")

    # Get conversation summary
    print("\nConversation summary:")
    summary = await manager.get_conversation_summary()
    print(summary)

    # Export memories
    print("\nExporting memories:")
    export_data = await manager.export_memories(format="dict")
    print(f"Exported {len(export_data['messages'])} messages and "
          f"{len(export_data['memories'])} memories")

    # Clear and import
    await manager.clear_memory()
    print("\nCleared memory")

    await manager.import_memories(export_data)
    print("Imported memories back")

    # Demonstrate time window
    print("\nMessages in last hour:")
    recent_messages = await manager.get_memory_window(
        start_time=datetime.utcnow() - timedelta(hours=1)
    )
    for msg in recent_messages:
        print(f"{msg.role}: {msg.content}")

    # Memory maintenance
    await manager.maintain_memory(
        max_size=100,
        min_importance=0.5
    )
    print("\nMaintained memory")

    # Get final stats
    stats = await manager.memory.get_stats()
    print("\nFinal memory stats:")
    print(stats)


if __name__ == "__main__":
    asyncio.run(main())