# Core Configuration (`src/settings.py`)

The settings module is the single source of truth for all application-wide configuration and environmental variables. It leverages modern Python tooling via `pydantic-settings`.

## Components

### `Settings` Class
A `BaseSettings` model that automatically type-checks and validates environment variables sourced from `.env` or from Docker compose.

**Fields:**
- `app_name`, `host`, `port`, `reload`: Basic API server setup.
- `discord_token`: A `SecretStr` storing the authentication token for the Discord bot.
- `mongodb_uri`: A `SecretStr` containing the connection string for the `AsyncIOMotorClient`.
- `mongodb_database_name`: Defaults to `"content_machine"`. 

**Validation:**
The `check_secrets_exist` validator ensures that the required tokens (`DISCORD_TOKEN`, `MONGODB_URI`) are explicitly injected at boot time, preventing silent deployment failures.

---

## Accessing Settings

The module employs a singleton pattern to optimize boot performance and prevent parsing the environment repeatedly across imports.

```python
from src.settings import get_settings

# Calling this caches the settings on the first run
settings = get_settings()

print(settings.app_name) # "Content Machine"

# To access SecretStr values, call `.get_secret_value()`
token = settings.discord_token.get_secret_value()
```

## Centralized Logging

The module also provisions application-wide logging functionality via the `get_logger()` singleton wrapper. Logging outputs to the standard stream (stdout) so Docker can easily pipe the container outputs.

```python
from src.settings import get_logger

logger = get_logger()
logger.info("Application starting...")
```
