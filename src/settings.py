from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    app_name: str = "Content Machine"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

    discord_token: str = Field(..., alias="DISCORD_TOKEN")

    @field_validator("discord_token")
    @classmethod
    def check_token_exists(cls, v):
        if not v:
            raise ValueError("DISCORD_TOKEN is not set")
        return v

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )


_settings = None

def get_settings():
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
