# Content Machine

A developer-focused pipeline for ingesting chat-platform messages and making them available to downstream agent systems.

## What it does

Chat platforms implement a shared `BaseChannel` interface. Each incoming event is normalised into a common message representation, persisted to MongoDB, and managed through a FastAPI service. Discord is the first supported channel.

```text
Chat platform → channel adapter → normalised message → MongoDB → agent-ready pipeline
```

## Stack

- FastAPI for service lifecycle and background work
- `discord.py` for the Discord adapter
- MongoDB + Motor for persistence
- Pydantic Settings for typed configuration

## Run locally

Copy `.env.example` to `.env` and set a real Discord token and MongoDB connection details. Do not commit that file.

```bash
docker compose up
```

The repository requires Python 3.12+ for local development outside Docker.

## Documentation map

- [Docker quickstart](docs/docker_compose_quickstart.md)
- [Channels](docs/channels.md)
- [Message persistence](docs/memory.md)
- [Server lifecycle](docs/server.md)
- [Configuration](docs/core_settings.md)

## Status and boundaries

This is an extensible ingestion foundation, not a public hosted service. A real deployment needs protected secrets, a managed MongoDB instance, and platform-specific OAuth/webhook configuration before exposing it to users.

## License

MIT
