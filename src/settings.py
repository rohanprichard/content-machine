from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    app_name: str = "Content Machine"
    host: str = "0.0.0.0"
    port: int = 8000
    discord_token: str | None = None

    def _load_env_variables(self):
        self.app_name = os.getenv("APP_NAME", self.app_name)
        self.host = os.getenv("HOST", self.host)
        self.port = os.getenv("PORT", self.port)
        self.discord_token = os.getenv("DISCORD_TOKEN", self.discord_token)

    def _validate_env_variables(self):
        if not self.discord_token:
            raise ValueError("DISCORD_TOKEN is not set")
    
    def __init__(self):
        self._load_env_variables()
        self._validate_env_variables()
        super().__init__()
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = None


def get_settings():
    global settings
    if settings is None:
        settings = Settings()
    return settings
