from src.memory.main import MongoDBManager
from src.settings import get_logger

logger = get_logger()


async def save_message(message_data: dict) -> str:
    """
    Save a message to the database.
    """
    db = MongoDBManager.get_database()
    collection = db.messages
    result = await collection.insert_one(message_data)
    logger.info(f"Saved message with _id: {result.inserted_id}")
    return str(result.inserted_id)


async def read_messages(channel_type: str = "discord") -> list:
    """
    Read all messages from the database.
    """
    db = MongoDBManager.get_database()
    collection = db.messages
    cursor = collection.find()
    return [doc for doc in cursor]
