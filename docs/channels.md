# Input Channels (`src/channel/`)

The Channels module provides an extensible framework for integrating different chat platforms (like Discord, Slack, etc.) into the Content Machine application. It relies on a uniform interface so that the core backend only has to deal with one unified message format.

## The Standard Message

Located in `src/channel/base.py`, the `Message` class defines the standard, platform-agnostic structure that all channels must map their events into:

```python
class Message(BaseModel):
    content: str
    sender_id: str
    timestamp: datetime = datetime.now()
    metadata: Optional[dict] = None
```

## `BaseChannel` Interface

`BaseChannel` acts as an Abstract Base Class (`ABC`). Any new platform added to the project must subclass it and implement methods corresponding to your application's lifecycle:

- `connect_on_startup()`: Called once on FastAPI boot.
- `disconnect_on_shutdown()`: Cleanly shuts down the socket.
- `on_message()`: Handles incoming data streams payload events.
- `process_message()`: **(Provided)** A built-in utility that intercepts a normalized `Message` and automatically persists it to the MongoDB database without requiring reimplementation across subclasses.

---

## Discord Implementation

The primary channel currently implemented is `src/channel/discord.py`.

### Multiple Inheritance
The `DiscordChannel` uses multiple inheritance:
```python
class DiscordChannel(Client, BaseChannel):
```
It inherits networking capabilities from `discord.py`'s built-in `Client` and standardizes its hooks to conform to `BaseChannel`.

### Passing Events to Database
When the WebSocket emits an `on_message` event, the bot immediately reformats the `discord_message` into a normalized `Message`, capturing the essential IDs and stripping away platform-specific noise. 

```python
standard_msg = NormalizedMessage(
    content=discord_message.content,
    sender_id=str(discord_message.author.id),
    metadata={
        "channel_id": discord_message.channel.id,
        "guild_id": discord_message.guild.id
    }
)

# This invokes the base method to write right to the memory DB
await process_message(standard_msg, channel_type="discord")
```

## Creating New Channels

If you were to add Telegram:
1. Subclass `BaseChannel` in `src/channel/telegram.py`.
2. Connect to the Telegram API inside `connect_on_startup()`.
3. In its message listener, transform the Telegram payload into the shared `Message` format and call `process_message()`. This instantly integrates the new platform with your database.
