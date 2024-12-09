"""Composio authentication manager."""

import os
import json
import logging
from typing import Optional, Dict, Any
import httpx
from pathlib import Path
import jwt
from datetime import datetime, timedelta

from .exceptions import ComposioAuthError

logger = logging.getLogger(__name__)

class ComposioAuthManager:
    """Manages Composio authentication and session handling."""
    
    def __init__(
        self,
        api_url: Optional[str] = None,
        token_path: Optional[str] = None
    ):
        """Initialize auth manager.
        
        Args:
            api_url: Composio API URL
            token_path: Path to store auth tokens
        """
        self.api_url = api_url or os.getenv("COMPOSIO_API_URL", "https://api.composio.dev")
        self.token_path = token_path or Path.home() / ".composio" / "auth.json"
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        self._session_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login to Composio with admin credentials.
        
        Args:
            email: Admin email
            password: Admin password
            
        Returns:
            Dict containing auth tokens and user info
            
        Raises:
            ComposioAuthError: If authentication fails
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.api_url}/auth/login",
                    json={
                        "email": email,
                        "password": password
                    }
                )
                response.raise_for_status()
                auth_data = response.json()
                
                # Store tokens
                self._session_token = auth_data["session_token"]
                self._refresh_token = auth_data["refresh_token"]
                
                # Save tokens to file
                self._save_tokens()
                
                return auth_data
                
            except httpx.HTTPError as e:
                raise ComposioAuthError(f"Login failed: {str(e)}")
                
    async def refresh_session(self) -> Dict[str, Any]:
        """Refresh the session using refresh token.
        
        Returns:
            Dict containing new auth tokens
            
        Raises:
            ComposioAuthError: If refresh fails
        """
        if not self._refresh_token:
            raise ComposioAuthError("No refresh token available")
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.api_url}/auth/refresh",
                    headers={"Authorization": f"Bearer {self._refresh_token}"}
                )
                response.raise_for_status()
                auth_data = response.json()
                
                # Update tokens
                self._session_token = auth_data["session_token"]
                self._refresh_token = auth_data["refresh_token"]
                
                # Save updated tokens
                self._save_tokens()
                
                return auth_data
                
            except httpx.HTTPError as e:
                raise ComposioAuthError(f"Session refresh failed: {str(e)}")
                
    async def logout(self) -> None:
        """Logout and invalidate current session."""
        if self._session_token:
            async with httpx.AsyncClient() as client:
                try:
                    await client.post(
                        f"{self.api_url}/auth/logout",
                        headers={"Authorization": f"Bearer {self._session_token}"}
                    )
                except httpx.HTTPError:
                    pass  # Ignore errors during logout
                    
        # Clear tokens
        self._session_token = None
        self._refresh_token = None
        
        # Remove stored tokens
        if self.token_path.exists():
            self.token_path.unlink()
            
    def get_session_token(self) -> Optional[str]:
        """Get current session token."""
        return self._session_token
        
    def is_logged_in(self) -> bool:
        """Check if user is logged in with valid session."""
        if not self._session_token:
            return False
            
        try:
            # Decode token to check expiration
            payload = jwt.decode(
                self._session_token,
                options={"verify_signature": False}
            )
            exp = datetime.fromtimestamp(payload["exp"])
            return exp > datetime.utcnow()
            
        except (jwt.InvalidTokenError, KeyError):
            return False
            
    def _save_tokens(self) -> None:
        """Save auth tokens to file."""
        token_data = {
            "session_token": self._session_token,
            "refresh_token": self._refresh_token
        }
        
        with open(self.token_path, "w") as f:
            json.dump(token_data, f)
            
    def _load_tokens(self) -> None:
        """Load auth tokens from file."""
        if not self.token_path.exists():
            return
            
        try:
            with open(self.token_path) as f:
                token_data = json.load(f)
                self._session_token = token_data.get("session_token")
                self._refresh_token = token_data.get("refresh_token")
                
        except (json.JSONDecodeError, KeyError):
            logger.warning("Failed to load auth tokens")
            self.token_path.unlink()
