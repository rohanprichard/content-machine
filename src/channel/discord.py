from discord import Client, Intents, Message

from src.settings import get_settings, get_logger
from src.channel.base import BaseChannel, Message as NormalizedMessage
from src.channel.utils import process_message

settings = get_settings()
logger = get_logger()


class DiscordChannel(Client, BaseChannel):
    """Discord channel implementation"""

    def __init__(self, **kwargs) -> None:
        intents = Intents.default()
        intents.message_content = True

        Client.__init__(self, intents=intents, **kwargs)
        BaseChannel.__init__(self)

    async def connect_on_startup(self) -> None:
        logger.info("starting discord channel")
        await self.start(token=settings.discord_token.get_secret_value(), reconnect=True)

    async def on_ready(self):
        self.is_connected = True
        logger.info(f"logged in as: {self.user}")

    async def on_message(self, discord_message: Message) -> bool:  # type: ignore[override]
        if discord_message.author == self.user:
            return False

        async with discord_message.channel.typing():
            logger.info(f"message received from user: {discord_message.author.name}")
            standard_msg = NormalizedMessage(
                content=discord_message.content,
                sender_id=str(discord_message.author.id),
                metadata={
                    "channel_id": discord_message.channel.id,
                    "guild_id": discord_message.guild.id if discord_message.guild else None,
                },
            )

            reply = await process_message(standard_msg, channel_type="discord")
            await discord_message.channel.send(reply.content)

            return True

        return False

    async def disconnect_on_shutdown(self) -> None:
        if self.is_connected:
            await self.close()
            self.is_connected = False
        logger.info("discord channel disconnected")
