from abc import ABC, abstractmethod
from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    """Standardized message format across all channels"""
    content: str
    sender_id: str
    timestamp: datetime = datetime.now()
    metadata: Optional[dict] = None


class BaseChannel(ABC):
    def __init__(self) -> None:
        self.is_connected = False

    @abstractmethod
    async def start(self) -> None:
        """Initialize the connection and keep it alive."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Cleanly close the connection."""
        pass

    @abstractmethod
    async def on_message(self, message: Message) -> bool:
        """Action to perform when a message is received."""
        pass
