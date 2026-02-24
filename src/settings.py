from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr, field_validator
from uuid import uuid4
import logging


class Settings(BaseSettings):
    app_name: str = "Content Machine"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    discord_token: SecretStr = Field(..., alias="DISCORD_TOKEN")

    mongodb_uri: SecretStr = Field(..., alias="MONGODB_URI")
    mongodb_database_name: str = Field("content_machine", alias="MONGODB_DATABASE_NAME")

    @field_validator("discord_token", "mongodb_uri")
    @classmethod
    def check_secrets_exist(cls, v, info):
        if not v or v.get_secret_value().strip() == "":
            raise ValueError(f"{info.field_name} is not set.")
        return v

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


_settings = None
_logger = None


def get_settings():
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def get_logger():
    global _logger
    if _logger is None:
        _logger = logging.getLogger(__name__)
        _logger.setLevel(logging.INFO)
        _logger.addHandler(logging.StreamHandler())
    return _logger


def get_uuid():
    return str(uuid4())
