# Server Application (`src/server.py`)

This module initializes the FastAPI web server and orchestrates the application's lifecycle, binding background services (like the Discord bot thread) to the API uptime.

## FastAPI Application

The application is heavily rooted in `asyncio`. It exposes core HTTP endpoints (such as health checks on the root path `/`) while managing independent background tasks.

## Lifespan & Background Tasks

The app uses standard FastAPI `@asynccontextmanager` lifespans to weave setup and teardown commands gracefully alongside the server itself.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup: runs BEFORE the first HTTP request is accepted
    app.state.discord_channel = DiscordChannel()
    bot_task = asyncio.create_task(app.state.discord_channel.connect_on_startup())

    yield # Normal server operation

    # Teardown: runs AFTER the server begins gracefully shutting down
    await app.state.discord_channel.disconnect_on_shutdown()
    bot_task.cancel()
```

### Flow Breakdown:
1. When the FastAPI core boots, it binds a new instance of `DiscordChannel` to its global `app.state`.
2. It spawns the Discord bot in the background using `asyncio.create_task`, which prevents the bot's infinitely running connection loop from blocking the main thread (thereby still allowing inbound web requests).
3. If the process is halted (like stopping a Docker container), FastAPI signals the thread, cleanly disconnects the Discord socket, and cancels the loop task so data isn't mangled.

## Healthchecks

The base `/` endpoint functions as a lightweight liveness probe. It actively confirms both the API and the background Discord tasks are healthy.

```json
{
  "status": "ok",
  "discord": true
}
```
