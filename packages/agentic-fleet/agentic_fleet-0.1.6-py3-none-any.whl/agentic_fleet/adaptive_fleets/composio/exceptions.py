"""Composio-specific exceptions."""

class ComposioError(Exception):
    """Base class for Composio errors."""
    pass

class ComposioAuthError(ComposioError):
    """Authentication error."""
    pass

class ComposioAPIError(ComposioError):
    """API error."""
    pass

class ComposioRateLimitError(ComposioError):
    """Rate limit exceeded error."""
    pass
