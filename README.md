# content-machine

An extensible framework for ingesting messages from chat platforms and routing them into a persistent, agent-ready pipeline.

Chat platforms (Discord today, more to come) plug into a shared `BaseChannel` interface and normalize every event into one standard `Message` format. A FastAPI server manages the platform connections' lifecycle, and MongoDB persists the flow of messages for downstream processing by the agent layer.

## Stack

- FastAPI — server + background task orchestration
- discord.py — first channel implementation
- MongoDB (Motor, async) — message persistence
- Pydantic Settings — typed, validated config from `.env`

## Running it

```bash
docker compose up
```

See `docs/` for a walkthrough of each module: [`channels`](docs/channels.md), [`memory`](docs/memory.md), [`server`](docs/server.md), [`core_settings`](docs/core_settings.md).
