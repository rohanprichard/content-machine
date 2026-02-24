from motor.motor_asyncio import AsyncIOMotorClient
from src.settings import get_settings, get_logger


settings = get_settings()
logger = get_logger()


class MongoDBManager:
    client: AsyncIOMotorClient | None = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls.client is None:
            logger.info("initializing mongodb connection")
            cls.client = AsyncIOMotorClient(settings.mongodb_uri.get_secret_value())
        return cls.client

    @classmethod
    def get_database(cls):
        client = cls.get_client()
        return client[settings.mongodb_database_name]

    @classmethod
    def close(cls):
        if cls.client:
            cls.client.close()
            cls.client = None
            logger.info("mongodb connection closed")
