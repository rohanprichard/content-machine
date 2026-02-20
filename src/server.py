import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.channel.discord import DiscordChannel

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    app.state.discord_channel = DiscordChannel()
    bot_task = asyncio.create_task(app.state.discord_channel.start())
    
    yield
    
    await app.state.discord_channel.disconnect()
    bot_task.cancel()

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    is_up = app.state.discord_channel.is_connected
    return {"status": "ok", "discord": is_up}