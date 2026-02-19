from abc import ABC, abstractmethod
from typing import Any, List, Optional
from datetime import datetime
from pydantic import BaseModel


class ChannelConfig(BaseModel):
    """Configuration data for a channel instance"""
    id: str
    name: str
    type: str
    credentials: dict


class Message(BaseModel):
    """Standardized message format across all channels"""
    content: str
    sender_id: str
    timestamp: datetime = datetime.now()
    metadata: Optional[dict] = None


class BaseChannel(ABC):
    """
    Abstract base class that defines the contract for all communication channels.
    """
    
    def __init__(self, config: ChannelConfig) -> None:
        self.config = config
        self.is_connected = False
        self.client = None

    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the channel provider."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Cleanly close the connection."""
        pass

    @abstractmethod
    async def on_message(self, message: Message) -> bool:
        """Handle an incoming message."""
        pass
