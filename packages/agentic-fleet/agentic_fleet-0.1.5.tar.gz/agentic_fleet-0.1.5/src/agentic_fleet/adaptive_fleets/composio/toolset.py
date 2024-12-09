"""Composio API toolset for managing connections and integrations."""

import os
from enum import Enum
from typing import Optional

class App(str, Enum):
    """Supported Composio apps."""
    GMAIL = "gmail"
    OUTLOOK = "outlook"
    SLACK = "slack"

class ConnectionRequest:
    """Represents a connection request to a third-party app."""
    
    def __init__(self, redirect_url: str, connection_status: str):
        """Initialize the connection request."""
        self.redirectUrl = redirect_url
        self.connectionStatus = connection_status

class ComposioToolSet:
    """Composio API toolset for managing connections and integrations."""
    
    def __init__(self):
        """Initialize the toolset with API configuration."""
        self.api_key = os.getenv("COMPOSIO_API_KEY")
        self.api_url = os.getenv("COMPOSIO_API_URL")
        self.default_redirect_url = os.getenv("COMPOSIO_REDIRECT_URL")
        
        if not self.api_key or not self.api_url:
            raise ValueError("COMPOSIO_API_KEY and COMPOSIO_API_URL must be set")

    async def initiate_connection(self, entity_id: str, app: App, redirect_url: Optional[str] = None):
        """Initiate a new connection for a user.
        
        Args:
            entity_id: Unique identifier for the user
            app: The app to connect to (e.g., Gmail, Outlook)
            redirect_url: Optional URL to redirect to after authentication. If not provided,
                         will use COMPOSIO_REDIRECT_URL from environment variables.
            
        Returns:
            ConnectionRequest object containing the redirect URL and connection status
            
        Raises:
            ValueError: If no redirect URL is provided and COMPOSIO_REDIRECT_URL is not set
        """
        # Use provided redirect_url or fall back to default
        final_redirect_url = redirect_url or self.default_redirect_url
        if not final_redirect_url:
            raise ValueError(
                "redirect_url must be provided either as an argument or "
                "through COMPOSIO_REDIRECT_URL environment variable"
            )
        
        # In a real implementation, this would make an API call to Composio
        return ConnectionRequest(
            redirect_url=f"{self.api_url}/oauth/connect?app={app}&entity={entity_id}&redirect={final_redirect_url}",
            connection_status="initiated"
        )
