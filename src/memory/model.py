from typing import Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

from src.channel.base import Message as ChannelMessage


class DBMessage(BaseModel):
    """
    Model for messages stored in the database.
    """

    id: Optional[Any] = Field(default=None, alias="_id")
    content: str
    sender_id: str
    timestamp: datetime
    metadata: Optional[dict] = None
    channel_type: str

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }

    @classmethod
    def from_channel_message(
        cls, message: ChannelMessage, channel_type: str = "discord"
    ) -> "DBMessage":
        """
        Convert a ChannelMessage to a DBMessage.
        """
        return cls(
            content=message.content,
            sender_id=message.sender_id,
            timestamp=message.timestamp,
            metadata=message.metadata,
            channel_type=channel_type,
        )
