"""Test suite for CaptainAgent."""

import pytest
from typing import List, Dict, Any

from agentic_fleet import CaptainAgent, SpecialistAgent, Tool
from agentic_fleet.base import BaseAgent
from agentic_fleet.captain import TaskResult

class MockTool(Tool):
    """Mock tool for testing."""
    def execute(self, **kwargs: Any) -> Any:
        return {"status": "success", "data": kwargs}

class MockSpecialist(SpecialistAgent):
    """Mock specialist agent for testing."""
    def execute(self, task: str, context: Dict[str, Any] = None) -> Any:
        return {"status": "success", "task": task, "context": context}
        
    def validate_task(self, task: str, context: Dict[str, Any] = None) -> bool:
        """Mock task validation."""
        return True

@pytest.fixture
def mock_tools() -> List[Tool]:
    """Create mock tools for testing."""
    return [
        MockTool(name="tool1", description="Test tool 1"),
        MockTool(name="tool2", description="Test tool 2")
    ]

@pytest.fixture
def mock_specialists() -> List[SpecialistAgent]:
    """Create mock specialist agents for testing."""
    return [
        MockSpecialist(
            name="specialist1",
            system_message="Test specialist 1",
            tools=[]
        ),
        MockSpecialist(
            name="specialist2", 
            system_message="Test specialist 2",
            tools=[]
        )
    ]

@pytest.fixture
def captain(mock_tools, mock_specialists) -> CaptainAgent:
    """Create a CaptainAgent instance for testing."""
    return CaptainAgent(
        name="test_captain",
        system_message="Test captain agent",
        tools=mock_tools,
        specialist_agents=mock_specialists
    )

def test_captain_initialization(captain: CaptainAgent):
    """Test CaptainAgent initialization."""
    assert isinstance(captain, BaseAgent)
    assert captain.name == "test_captain"
    assert len(captain.tools) == 2
    assert len(captain.specialist_agents) == 2
    assert captain.max_iterations == 5
    assert captain.validation_threshold == 0.8

def test_create_task_plan(captain: CaptainAgent):
    """Test task plan creation."""
    task = "Test task"
    context = {"param": "value"}
    
    plan = captain.create_task_plan(task, context)
    
    assert isinstance(plan.steps, list)
    assert isinstance(plan.success_criteria, list)
    assert isinstance(plan.required_tools, list)
    assert isinstance(plan.estimated_completion_time, float)

def test_validate_result(captain: CaptainAgent):
    """Test result validation."""
    result = {"output": "test"}
    criteria = ["Output should be present"]
    
    score = captain.validate_result(result, criteria)
    assert 0 <= score <= 1

def test_delegate_task(captain: CaptainAgent):
    """Test task delegation to specialist agents."""
    task = {"action": "test"}
    agent_name = "specialist1"
    
    result = captain.delegate_task(task, agent_name)
    assert result["status"] == "success"
    assert result["task"] == task

def test_execute_task(captain: CaptainAgent):
    """Test full task execution."""
    task = "Test task"
    context = {"param": "value"}
    
    result = captain.execute(task, context)
    assert isinstance(result, TaskResult)
    assert hasattr(result, "success")
    assert hasattr(result, "output")
    assert hasattr(result, "execution_time")
