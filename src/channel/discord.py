from .base import BaseChannel, Message
from typing import List
import discord

from settings import get_settings

settings = get_settings()


class DiscordChannel(BaseChannel):
    def connect(self) -> bool:
        print("Connecting to Discord...")
        discord.init(self.config.credentials.get('token'))
        self.client = discord.Client(token=settings.discord_token)
        self.is_connected = True
        return True

    def disconnect(self) -> None:
        print("Disconnecting from Discord...")
        self.is_connected = False

    def send_message(self, message: Message) -> bool:
        if not self.is_connected:
            self.connect()
        print(f"Posting to Discord channel {self.config.id}")
        return True

    def receive_messages(self, limit: int = 10) -> List[Message]:
        return []