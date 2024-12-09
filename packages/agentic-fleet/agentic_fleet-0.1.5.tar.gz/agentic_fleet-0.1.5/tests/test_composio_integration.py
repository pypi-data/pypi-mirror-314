"""Test Composio API integration."""

import pytest
import os
from dotenv import load_dotenv
from agentic_fleet.adaptive_fleets.composio import (
    ComposioClient,
    ComposioAuthFleet,
    ComposioSWEFleet,
)
from agentic_fleet.adaptive_fleets.composio.exceptions import (
    ComposioAuthError,
    ComposioAPIError,
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
async def client():
    """Create Composio client for testing."""
    client = ComposioClient()
    yield client
    await client.close()

@pytest.mark.asyncio
async def test_client_initialization(client):
    """Test that client initializes successfully."""
    assert client is not None
    assert client.config.api_key == os.getenv("COMPOSIO_API_KEY")
    assert client.config.api_url == os.getenv("COMPOSIO_API_URL")

@pytest.mark.asyncio
async def test_auth_fleet():
    """Test authentication fleet functionality."""
    protocol = RedisProtocol()
    auth_fleet = ComposioAuthFleet(protocol=protocol)
    
    # Create an authentication agent
    agent = await auth_fleet.create_agent(
        name="test_auth_agent",
        capabilities=["token_validation"]
    )
    
    assert agent is not None
    print(f"Created auth agent: {agent}")
    
    # Test token validation
    result = await auth_fleet.execute_task(
        agent=agent,
        task="Validate test token",
        context={"token": "test_token"}
    )
    
    assert result is not None
    print(f"Auth task result: {result}")

@pytest.mark.asyncio
async def test_swe_fleet():
    """Test software engineering fleet functionality."""
    protocol = RedisProtocol()
    swe_fleet = ComposioSWEFleet(protocol=protocol)
    
    # Create a code review agent
    agent = await swe_fleet.create_agent(
        name="test_swe_agent",
        capabilities=["code_review"]
    )
    
    assert agent is not None
    print(f"Created SWE agent: {agent}")
    
    # Test code review
    code_snippet = """
    def add(a, b):
        return a + b
    """
    
    result = await swe_fleet.execute_task(
        agent=agent,
        task="Review code snippet",
        context={"code": code_snippet}
    )
    
    assert result is not None
    print(f"SWE task result: {result}")

@pytest.mark.asyncio
async def test_error_handling(client):
    """Test error handling with invalid API key."""
    # Create client with invalid API key
    invalid_client = ComposioClient(
        config=type(client.config)(
            api_key="invalid_key",
            api_url=client.config.api_url
        )
    )
    
    with pytest.raises(ComposioAuthError):
        await invalid_client.create_agent(
            agent_type="test",
            parameters={}
        )
