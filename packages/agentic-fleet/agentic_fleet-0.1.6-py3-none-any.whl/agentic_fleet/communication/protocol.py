"""Base communication protocol."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
import json
import logging

logger = logging.getLogger(__name__)

class MessageType(str, Enum):
    """Types of messages between agents."""
    TASK = "task"
    RESULT = "result"
    STATUS = "status"
    CONTROL = "control"
    ERROR = "error"
    METRIC = "metric"

class Message(BaseModel):
    """Message between agents."""
    type: MessageType
    sender: str
    receiver: Optional[str] = None
    content: Dict[str, Any]
    timestamp: float
    correlation_id: Optional[str] = None
    priority: int = 0
    
    def to_json(self) -> str:
        """Convert message to JSON string."""
        return self.model_dump_json()
    
    @classmethod
    def from_json(cls, data: str) -> "Message":
        """Create message from JSON string."""
        return cls.model_validate_json(data)

class CommunicationProtocol(ABC):
    """Base class for communication protocols."""
    
    @abstractmethod
    async def connect(self) -> None:
        """Connect to communication backend."""
        pass
        
    @abstractmethod
    async def disconnect(self) -> None:
        """Disconnect from communication backend."""
        pass
        
    @abstractmethod
    async def send(self, message: Message) -> None:
        """Send message.
        
        Args:
            message: Message to send
        """
        pass
        
    @abstractmethod
    async def receive(self) -> Optional[Message]:
        """Receive message.
        
        Returns:
            Received message if available
        """
        pass
        
    @abstractmethod
    async def subscribe(self, topics: List[str]) -> None:
        """Subscribe to topics.
        
        Args:
            topics: Topics to subscribe to
        """
        pass
        
    @abstractmethod
    async def unsubscribe(self, topics: List[str]) -> None:
        """Unsubscribe from topics.
        
        Args:
            topics: Topics to unsubscribe from
        """
        pass
        
    async def broadcast(self, message: Message) -> None:
        """Broadcast message to all subscribers.
        
        Args:
            message: Message to broadcast
        """
        message.receiver = None
        await self.send(message)
        
    async def request_response(
        self,
        message: Message,
        timeout: float = 5.0,
    ) -> Optional[Message]:
        """Send request and wait for response.
        
        Args:
            message: Request message
            timeout: Timeout in seconds
            
        Returns:
            Response message if received
        """
        await self.send(message)
        
        # Implementation would wait for response
        return None
