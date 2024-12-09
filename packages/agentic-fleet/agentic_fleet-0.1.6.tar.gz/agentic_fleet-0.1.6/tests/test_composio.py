"""Test Composio integration."""

import asyncio
import os
from dotenv import load_dotenv
import pytest

from agentic_fleet.adaptive_fleets.composio.client import ComposioClient
from agentic_fleet.adaptive_fleets.composio import ComposioAuthFleet, ComposioSWEFleet

@pytest.fixture
async def client():
    """Create Composio client."""
    load_dotenv()
    client = ComposioClient()
    yield client
    await client.close()

@pytest.fixture
async def auth_fleet():
    """Create auth fleet."""
    fleet = ComposioAuthFleet()
    yield fleet
    # Cleanup would go here

@pytest.fixture
async def swe_fleet():
    """Create SWE fleet."""
    fleet = ComposioSWEFleet()
    yield fleet
    # Cleanup would go here

@pytest.mark.asyncio
async def test_client_connection(client):
    """Test client can connect to Composio."""
    # Create a test agent
    agent = await client.create_agent(
        agent_type="software_engineer",
        parameters={
            "role": "test",
            "capabilities": ["testing"],
            "model": "gpt-4",
        },
    )
    assert agent["id"], "Agent creation failed"

@pytest.mark.asyncio
async def test_auth_fleet(auth_fleet):
    """Test auth fleet functionality."""
    context = {
        "auth_requirements": ["oauth2"],
        "scope": "read write",
    }
    
    # Test adaptation
    await auth_fleet.adapt(context)
    
    # Test execution
    result = await auth_fleet.execute(
        task="Verify OAuth2 token",
        context=context,
    )
    assert result, "Auth task execution failed"

@pytest.mark.asyncio
async def test_swe_fleet(swe_fleet):
    """Test SWE fleet functionality."""
    context = {
        "code_tasks": ["code_review"],
        "code": """
def add(a: int, b: int) -> int:
    return a + b
        """,
    }
    
    # Test adaptation
    await swe_fleet.adapt(context)
    
    # Test execution
    result = await swe_fleet.execute(
        task="Review code quality",
        context=context,
    )
    assert result, "SWE task execution failed"
    
    # Test evaluation
    score = await swe_fleet.evaluate(result, context)
    assert 0 <= score <= 1, "Invalid evaluation score"

if __name__ == "__main__":
    asyncio.run(test_client_connection(ComposioClient()))
