"""Test Composio Reasoning Fleet functionality."""

import pytest
import os
from unittest.mock import AsyncMock, patch, MagicMock
from dotenv import load_dotenv
from agentic_fleet.adaptive_fleets.composio.reasoning_fleet import (
    ComposioReasoningFleet,
    ReasoningCapability,
)
from agentic_fleet.communication.redis_protocol import RedisProtocol

@pytest.fixture(autouse=True)
def load_env():
    """Load environment variables before tests."""
    load_dotenv()
    
    # Verify required env vars
    assert os.getenv("COMPOSIO_API_KEY"), "COMPOSIO_API_KEY not set"
    assert os.getenv("COMPOSIO_API_URL"), "COMPOSIO_API_URL not set"

@pytest.fixture
def mock_client():
    """Create mock Composio client."""
    client = MagicMock()
    client.create_agent = AsyncMock()
    client.execute_task = AsyncMock()
    return client

@pytest.fixture
def fleet(mock_client):
    """Create Composio reasoning fleet for testing."""
    protocol = RedisProtocol()
    fleet = ComposioReasoningFleet(protocol=protocol)
    fleet.client = mock_client
    return fleet

@pytest.mark.asyncio
async def test_create_agent_default_capabilities(fleet, mock_client):
    """Test creating a reasoning agent with default capabilities."""
    # Configure mock
    mock_agent = MagicMock()
    mock_agent.parameters = {
        "role": "reasoner",
        "capabilities": [ReasoningCapability.DEDUCTION],
        "model": "gpt-4"
    }
    mock_client.create_agent.return_value = mock_agent
    
    # Create agent
    agent = await fleet.create_agent(name="test_reasoner")
    
    # Verify agent configuration
    assert agent is not None
    assert agent.parameters["role"] == "reasoner"
    assert agent.parameters["capabilities"] == [ReasoningCapability.DEDUCTION]
    assert agent.parameters["model"] == "gpt-4"

@pytest.mark.asyncio
async def test_create_agent_custom_capabilities(fleet, mock_client):
    """Test creating a reasoning agent with custom capabilities."""
    # Define custom capabilities
    capabilities = [
        ReasoningCapability.INDUCTION,
        ReasoningCapability.ABDUCTION,
        ReasoningCapability.ANALOGY
    ]
    
    # Configure mock
    mock_agent = MagicMock()
    mock_agent.parameters = {
        "role": "reasoner",
        "capabilities": capabilities,
        "model": "gpt-4"
    }
    mock_client.create_agent.return_value = mock_agent
    
    # Create agent
    agent = await fleet.create_agent(
        name="test_reasoner",
        capabilities=capabilities
    )
    
    # Verify agent configuration
    assert agent is not None
    assert agent.parameters["role"] == "reasoner"
    assert agent.parameters["capabilities"] == capabilities
    assert agent.parameters["model"] == "gpt-4"

@pytest.mark.asyncio
async def test_create_agent_custom_parameters(fleet, mock_client):
    """Test creating a reasoning agent with custom parameters."""
    # Define custom parameters
    parameters = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.9,
        "max_tokens": 4000
    }
    
    # Configure mock
    mock_agent = MagicMock()
    mock_agent.parameters = {
        "role": "reasoner",
        "capabilities": [ReasoningCapability.DEDUCTION],
        **parameters
    }
    mock_client.create_agent.return_value = mock_agent
    
    # Create agent
    agent = await fleet.create_agent(
        name="test_reasoner",
        parameters=parameters
    )
    
    # Verify agent configuration
    assert agent is not None
    assert agent.parameters["role"] == "reasoner"
    assert agent.parameters["model"] == parameters["model"]
    assert agent.parameters["temperature"] == parameters["temperature"]
    assert agent.parameters["max_tokens"] == parameters["max_tokens"]

@pytest.mark.asyncio
async def test_execute_deduction_task(fleet, mock_client):
    """Test executing a deductive reasoning task."""
    # Configure mock agent
    mock_agent = MagicMock()
    mock_agent.parameters = {
        "role": "reasoner",
        "capabilities": [ReasoningCapability.DEDUCTION],
        "model": "gpt-4"
    }
    mock_client.create_agent.return_value = mock_agent
    
    # Configure mock task response
    mock_response = {
        "conclusion": "Socrates is mortal",
        "confidence": 0.95
    }
    mock_client.execute_task.return_value = mock_response
    
    # Create agent
    agent = await fleet.create_agent(
        name="test_reasoner",
        capabilities=[ReasoningCapability.DEDUCTION]
    )
    
    # Define task and context
    task = "Determine if Socrates is mortal"
    context = {
        "premises": [
            "All men are mortal",
            "Socrates is a man"
        ]
    }
    
    # Execute task
    result = await fleet.execute_task(
        agent=agent,
        task=task,
        context=context
    )
    
    # Verify result
    assert result is not None
    assert result["conclusion"] == "Socrates is mortal"
    assert result["confidence"] == 0.95

@pytest.mark.asyncio
async def test_analyze_data(fleet, mock_client):
    """Test analyzing data using a reasoning agent."""
    # Configure mock agent
    mock_agent = MagicMock()
    mock_agent.parameters = {
        "role": "reasoner",
        "capabilities": [
            ReasoningCapability.CAUSAL,
            ReasoningCapability.TEMPORAL
        ],
        "model": "gpt-4"
    }
    mock_client.create_agent.return_value = mock_agent
    
    # Configure mock analysis response
    mock_response = {
        "analysis": {
            "trend": "decreasing",
            "confidence": 0.85
        }
    }
    mock_client.execute_task.return_value = mock_response
    
    # Create agent
    agent = await fleet.create_agent(
        name="test_reasoner",
        capabilities=[
            ReasoningCapability.CAUSAL,
            ReasoningCapability.TEMPORAL
        ]
    )
    
    # Sample time series data
    data = {
        "timestamps": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "values": [100, 120, 90]
    }
    
    # Perform analysis
    result = await fleet.analyze(
        agent=agent,
        data=data,
        analysis_type="trend",
        parameters={"window_size": 3}
    )
    
    # Verify result
    assert result is not None
    assert result["analysis"]["trend"] == "decreasing"
    assert result["analysis"]["confidence"] == 0.85

@pytest.mark.asyncio
async def test_counterfactual_analysis(fleet, mock_client):
    """Test performing counterfactual analysis."""
    # Configure mock agent
    mock_agent = MagicMock()
    mock_agent.parameters = {
        "role": "reasoner",
        "capabilities": [ReasoningCapability.COUNTERFACTUAL],
        "model": "gpt-4"
    }
    mock_client.create_agent.return_value = mock_agent
    
    # Configure mock analysis response
    mock_response = {
        "analysis": {
            "counterfactual_outcome": "Company A would likely show 0-2% growth",
            "confidence": 0.8
        }
    }
    mock_client.execute_task.return_value = mock_response
    
    # Create agent
    agent = await fleet.create_agent(
        name="test_reasoner",
        capabilities=[ReasoningCapability.COUNTERFACTUAL]
    )
    
    # Define scenario and context
    scenario = {
        "actual": "Company A launched product X and saw 10% growth",
        "counterfactual": "What if Company A had not launched product X?"
    }
    
    # Perform analysis
    result = await fleet.analyze(
        agent=agent,
        data=scenario,
        analysis_type="counterfactual",
        parameters={"confidence_threshold": 0.8}
    )
    
    # Verify result
    assert result is not None
    assert "counterfactual_outcome" in result["analysis"]
    assert result["analysis"]["confidence"] == 0.8
