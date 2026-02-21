from abc import ABC, abstractmethod
from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel

from src.settings import get_logger

logger = get_logger()


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
    async def connect_on_startup(self) -> None:
        """Initialize the connection and keep it alive."""
        pass

    @abstractmethod
    async def disconnect_on_shutdown(self) -> None:
        """Close an active connection."""
        pass

    @abstractmethod
    async def on_message(self, message: Any) -> bool:
        """Handle a message received from the channel."""
        pass
