# EzyAgent: A Modern, Simple, and Powerful BaseAgent Framework

## Overview
EzyAgent is a next-generation agent framework designed to make AI agent development simple, observable, and reliable. By learning from the limitations of existing frameworks, we've created a solution that prioritizes developer experience while providing enterprise-grade features.

## 🌟 Key Features

### Simple Yet Powerful

```python
from ezyagentsdf import BaseAgent

# Create an agent in one line
agent = BaseAgent("gpt-4")

# Start chatting
response = await agent.chat("Explain quantum computing")


# Add tools easily
@agent.tool
async def search(query: str) -> str:
    """Search the web."""
    return await web_search(query)
```

### First-Class Async Support
```python
# Stream responses
async with BaseAgent() as agent:
    async for message in agent.stream_chat("Write a long story"):
        print(message)
        
# Parallel operations
async def process_queries(queries: List[str]):
    async with BaseAgent() as agent:
        tasks = [agent.chat(q) for q in queries]
        responses = await asyncio.gather(*tasks)
```

### Advanced Logging & Observability
```python
# Comprehensive logging setup
agent.logger.configure(
    format="json",
    outputs={
        "console": {"level": "INFO"},
        "file": {
            "path": "agent.log",
            "level": "DEBUG"
        },
        "cloudwatch": {
            "group": "agents",
            "stream": "production"
        }
    },
    metrics=["tokens", "latency", "costs"],
    trace_requests=True
)

# Access logs and metrics
print(agent.logger.get_metrics())
print(agent.logger.get_recent_traces())
```

### Robust Error Handling
```python
try:
    response = await agent.chat("Complex query")
except AgentError as e:
    print(f"Error Type: {e.error_type}")
    print(f"Provider Error: {e.provider_error}")
    print(f"Context: {e.context}")
    print(f"How to fix: {e.remediation}")
    print(f"Debug trace: {e.debug_info}")
```

### Intelligent State Management
```python
# Built-in memory and state management
agent.memory.save_state("user_preferences", preferences)
agent.memory.add_context("User is a developer")

# Access conversation history
history = agent.memory.get_chat_history()
context = agent.memory.get_relevant_context("query")

# Persistent storage
await agent.memory.save_to_disk("agent_state.json")
await agent.memory.load_from_disk("agent_state.json")
```

### Universal Provider Support
```python
# Easy provider switching
agent = BaseAgent(provider="openai")
agent = BaseAgent(provider="anthropic")
agent = BaseAgent(provider="ollama")

# Multiple providers with fallback
agent = BaseAgent(
    providers=["anthropic", "openai"],
    fallback_strategy="sequential"
)

# Custom provider configuration
agent = BaseAgent(
    provider="openai",
    config={
        "max_retries": 3,
        "timeout": 30,
        "rate_limit": 100
    }
)
```

## Why EzyAgent?

### Problems with Existing Frameworks

#### 1. Langchain
- ❌ Complex setup and steep learning curve
- ❌ Confusing abstractions
- ❌ Poor error handling
- ❌ Limited async support
- ✅ Extensive tool ecosystem
- ✅ Good documentation

#### 2. AutoGen
- ❌ Complex configuration
- ❌ Limited logging
- ❌ Difficult debugging
- ✅ Good multi-agent support
- ✅ Built-in caching

#### 3. Pydantic-AI
- ❌ Limited provider support
- ❌ Basic logging
- ❌ No state management
- ✅ Strong type validation
- ✅ Clean data structures

#### 4. LlamaIndex
- ❌ Complex for simple uses
- ❌ Heavy resource usage
- ❌ Confusing documentation
- ✅ Great RAG support
- ✅ Good data ingestion

#### 5. PhiData
- ❌ Limited features
- ❌ Basic logging
- ❌ Limited providers
- ✅ Simple API
- ✅ Clean implementation

### EzyAgent's Solutions

#### 1. Development Experience
- One-line setup
- Clear, concise API
- Comprehensive documentation
- Type hints everywhere
- Informative error messages
- IDE autocomplete support

#### 2. Observability
- Structured logging
- Request tracing
- Cost tracking
- Performance metrics
- Debug mode
- Custom metric support

#### 3. Reliability
- Automatic retries
- Smart rate limiting
- Provider fallbacks
- Error recovery strategies
- Validation checks

#### 4. Flexibility
- Easy extension
- Custom tools
- Provider agnostic
- State management
- Memory systems
- Custom implementations

#### 5. Performance
- Async by default
- Efficient resource usage
- Built-in caching
- Streaming support
- Parallel operations

## Architecture

```plaintext
ezyagent/
├── core/
│   ├── baseagent.py          # Base agent classes
│   ├── memory.py         # State management
│   ├── tools.py          # Tool management
│   └── providers/        # LLM providers
├── logging/
│   ├── logger.py         # Logging core
│   ├── formatters.py     # Log formatters
│   ├── handlers.py       # Output handlers
│   └── monitors.py       # Metrics
├── utils/
│   ├── errors.py         # Error handling
│   ├── validation.py     # Input validation
│   └── helpers.py        # Utilities
└── examples/             # Usage examples
```

## Installation

```bash
pip install ezyagent
```

## Quick Start

```python
from ezyagentsdf import BaseAgent

# Create an agent
agent = BaseAgent("gpt-4")

# Enable logging
agent.logger.configure(format="json", outputs=["console"])


# Add a tool
@agent.tool
async def search(query: str) -> str:
    """Search the web."""
    return await web_search(query)


# Chat with the agent
async def main():
    response = await agent.chat("Find recent news about AI")
    print(response)


# Run
asyncio.run(main())
```

## Documentation

Full documentation is available at [docs.ezyagent.dev](https://docs.ezyagent.dev)

## License

MIT License - feel free to use in your own projects!

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.