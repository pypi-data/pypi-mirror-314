"""Test Composio API integration using ComposioToolSet."""

import pytest
import os
from dotenv import load_dotenv
from agentic_fleet.adaptive_fleets.composio.toolset import (
    ComposioToolSet,
    App,
)

@pytest.fixture(autouse=True)
def load_env():
    """Load environment variables before tests."""
    load_dotenv()
    
    # Verify required env vars
    assert os.getenv("COMPOSIO_API_KEY"), "COMPOSIO_API_KEY not set"
    assert os.getenv("COMPOSIO_API_URL"), "COMPOSIO_API_URL not set"

@pytest.fixture
def toolset():
    """Create Composio toolset for testing."""
    return ComposioToolSet()

@pytest.mark.asyncio
async def test_initiate_connection_with_redirect(toolset):
    """Test initiating a new connection with explicit redirect URL."""
    # Test parameters
    redirect_url = "https://example.com/connection/success"
    entity_id = "test_user"
    app = App.GMAIL
    
    # Initiate connection
    connection_request = await toolset.initiate_connection(
        entity_id=entity_id,
        app=app,
        redirect_url=redirect_url
    )
    
    # Verify the connection request
    assert connection_request is not None
    assert connection_request.connectionStatus == "initiated"
    assert connection_request.redirectUrl.startswith(os.getenv("COMPOSIO_API_URL"))
    assert "/oauth/connect" in connection_request.redirectUrl
    assert f"app={app}" in connection_request.redirectUrl
    assert f"entity={entity_id}" in connection_request.redirectUrl
    assert f"redirect={redirect_url}" in connection_request.redirectUrl

@pytest.mark.asyncio
async def test_initiate_connection_with_env_redirect():
    """Test initiating a new connection using redirect URL from env."""
    # Set up environment
    os.environ["COMPOSIO_REDIRECT_URL"] = "https://default.example.com/callback"
    
    try:
        # Create toolset after setting environment variable
        toolset = ComposioToolSet()
        
        # Test parameters
        entity_id = "test_user"
        app = App.GMAIL
        
        # Initiate connection without explicit redirect_url
        connection_request = await toolset.initiate_connection(
            entity_id=entity_id,
            app=app
        )
        
        # Verify the connection request
        assert connection_request is not None
        assert connection_request.connectionStatus == "initiated"
        assert connection_request.redirectUrl.startswith(os.getenv("COMPOSIO_API_URL"))
        assert "/oauth/connect" in connection_request.redirectUrl
        assert f"app={app}" in connection_request.redirectUrl
        assert f"entity={entity_id}" in connection_request.redirectUrl
        assert f"redirect={os.getenv('COMPOSIO_REDIRECT_URL')}" in connection_request.redirectUrl
    finally:
        # Clean up environment
        os.environ.pop("COMPOSIO_REDIRECT_URL", None)

@pytest.mark.asyncio
async def test_initiate_connection_no_redirect():
    """Test that error is raised when no redirect URL is available."""
    # Save and remove any existing redirect URL
    saved_redirect_url = os.environ.pop("COMPOSIO_REDIRECT_URL", None)
    
    try:
        # Create toolset without COMPOSIO_REDIRECT_URL in env
        toolset = ComposioToolSet()
        
        # Verify that error is raised when no redirect_url is provided
        with pytest.raises(ValueError) as exc_info:
            await toolset.initiate_connection(
                entity_id="test_user",
                app=App.GMAIL
            )
        
        assert "redirect_url must be provided" in str(exc_info.value)
    finally:
        # Restore redirect URL if it existed
        if saved_redirect_url:
            os.environ["COMPOSIO_REDIRECT_URL"] = saved_redirect_url

@pytest.mark.asyncio
async def test_invalid_config():
    """Test toolset initialization with invalid config."""
    # Save current env vars
    api_key = os.getenv("COMPOSIO_API_KEY")
    api_url = os.getenv("COMPOSIO_API_URL")
    
    try:
        # Remove env vars
        os.environ.pop("COMPOSIO_API_KEY", None)
        os.environ.pop("COMPOSIO_API_URL", None)
        
        # Verify that toolset raises error
        with pytest.raises(ValueError):
            ComposioToolSet()
    finally:
        # Restore env vars
        if api_key:
            os.environ["COMPOSIO_API_KEY"] = api_key
        if api_url:
            os.environ["COMPOSIO_API_URL"] = api_url
