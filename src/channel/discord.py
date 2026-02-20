from typing import List
import discord

from src.settings import get_settings
from .base import BaseChannel, Message


settings = get_settings()


class DiscordChannel(BaseChannel):
    async def connect(self) -> bool:
        print("Connecting to Discord...")
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(token=settings.discord_token)
        self.is_connected = True
        return True

    async def disconnect(self) -> None:
        print("Disconnecting from Discord...")
        self.is_connected = False

    async def on_message(self, message: Message) -> bool:
        if not self.is_connected:
            self.connect()
        print(f"Received message from Discord: {message.content}")
        return True
