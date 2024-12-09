# Agentic Fleet

A powerful fleet of AI agents for complex reasoning and task execution, combining Tree of Thoughts reasoning with advanced agent orchestration capabilities.

## Features

- **Tree of Thoughts Reasoning**: Multi-agent reasoning system with beam search
- **CaptainAgent**: Advanced agent orchestration based on the paper "CaptainAgent: Building Reliable Autonomous Agents through Iterative Prompting"
- **Agent Fleet**: Extensible collection of specialized agents for different tasks
- **Tool Integration**: Rich set of tools and capabilities for agents
- **Modern Development**: Built with modern Python tools (uv, PDM)

## Installation

```bash
pip install agentic-fleet
```

## Quick Start

```python
from agentic_fleet import CaptainAgent, ReasoningAgent
from agentic_fleet.tools import CodeAnalysisTool, DataProcessingTool

# Initialize CaptainAgent with specialized tools
captain = CaptainAgent(
    name="project_captain",
    tools=[CodeAnalysisTool(), DataProcessingTool()],
    max_iterations=5
)

# Execute a complex task
result = captain.execute_task(
    "Analyze this codebase and suggest improvements",
    context={"repo_path": "./my_project"}
)

# Use reasoning agent for complex problem-solving
reasoner = ReasoningAgent(
    name="math_reasoner",
    beam_size=3,
    max_depth=5
)

solution = reasoner.solve("What is the optimal strategy for...")
```

## Architecture

The package consists of several key components:

1. **CaptainAgent**: Orchestrates complex tasks through iterative prompting
2. **ReasoningAgent**: Implements Tree of Thoughts for complex reasoning
3. **SpecialistAgents**: Task-specific agents (Coder, Analyst, etc.)
4. **Tools**: Extensible set of capabilities for agents
5. **Prompts**: Carefully crafted prompts for different scenarios

## Development

```bash
# Install development dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
black .
mypy .
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.
