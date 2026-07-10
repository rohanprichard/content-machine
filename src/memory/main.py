from motor.motor_asyncio import AsyncIOMotorClient

from src.settings import get_settings, get_logger


settings = get_settings()
logger = get_logger()


class MongoDBManager:
    client: AsyncIOMotorClient | None = None

    @classmethod
    def get_client(self) -> AsyncIOMotorClient:
        if self.client is None:
            logger.info("initializing mongodb connection")
            self.client = AsyncIOMotorClient(settings.mongodb_uri.get_secret_value())
        return self.client

    @classmethod
    def get_database(self):
        client = self.get_client()
        return client[settings.mongodb_database_name]

    @classmethod
    def close(self):
        if self.client:
            self.client.close()
            self.client = None
            logger.info("mongodb connection closed")
