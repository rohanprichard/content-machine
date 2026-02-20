from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


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
    
    def __init__(self) -> None:
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
