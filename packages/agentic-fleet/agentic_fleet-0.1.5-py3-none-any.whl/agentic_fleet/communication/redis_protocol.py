"""Redis communication protocol."""

from typing import Dict, Any, Optional, List
import redis.asyncio as redis
import json
import logging

from .protocol import CommunicationProtocol, Message, MessageType

logger = logging.getLogger(__name__)

class RedisProtocol(CommunicationProtocol):
    """Redis-based communication protocol."""
    
    def __init__(self, url: Optional[str] = None):
        """Initialize Redis protocol.
        
        Args:
            url: Redis URL, defaults to localhost
        """
        self.url = url or "redis://localhost:6379"
        self.client: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
        
    async def connect(self) -> None:
        """Connect to Redis."""
        self.client = redis.Redis.from_url(self.url)
        self.pubsub = self.client.pubsub()
        
    async def disconnect(self) -> None:
        """Disconnect from Redis."""
        if self.pubsub:
            await self.pubsub.close()
        if self.client:
            await self.client.close()
            
    async def send(self, message: Message) -> None:
        """Send message using Redis.
        
        Args:
            message: Message to send
        """
        if not self.client:
            raise RuntimeError("Not connected to Redis")
            
        channel = (
            message.receiver
            if message.receiver
            else "broadcast"
        )
        
        await self.client.publish(
            channel,
            message.to_json(),
        )
        
    async def receive(self) -> Optional[Message]:
        """Receive message from Redis.
        
        Returns:
            Received message if available
        """
        if not self.pubsub:
            raise RuntimeError("Not connected to Redis")
            
        message = await self.pubsub.get_message()
        if not message:
            return None
            
        try:
            return Message.from_json(message["data"])
        except Exception as e:
            logger.error(f"Failed to parse message: {e}")
            return None
            
    async def subscribe(self, topics: List[str]) -> None:
        """Subscribe to topics.
        
        Args:
            topics: Topics to subscribe to
        """
        if not self.pubsub:
            raise RuntimeError("Not connected to Redis")
            
        await self.pubsub.subscribe(*topics)
        
    async def unsubscribe(self, topics: List[str]) -> None:
        """Unsubscribe from topics.
        
        Args:
            topics: Topics to unsubscribe from
        """
        if not self.pubsub:
            raise RuntimeError("Not connected to Redis")
            
        await self.pubsub.unsubscribe(*topics)
