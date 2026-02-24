from src.memory.message import save_message
from src.memory.model import DBMessage
from src.channel.base import Message
from src.settings import get_logger, get_uuid


logger = get_logger()


async def process_message(message: Message, channel_type: str) -> Message:
    """
    Process a normalized message. Saves it to the database.
    """
    try:
        db_msg = DBMessage.from_channel_message(message, channel_type=channel_type)
        msg_id = await save_message(db_msg.model_dump(by_alias=True, exclude_none=True))

        return Message(**message.model_dump(by_alias=True, exclude_none=True))

    except Exception as e:
        logger.error(f"Failed to persist message: {e}")
        return Message(**message.model_dump(by_alias=True, exclude_none=True))
