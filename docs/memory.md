# Memory Module (`src/memory/`)

The Memory module integrates caching and persistent storage using MongoDB to track the flow of messages arriving from different channels.

## Database Management

`main.py` handles the underlying NoSQL interactions via `AsyncIOMotorClient`, exposing a singleton manager.

### `MongoDBManager`

```python
class MongoDBManager:
    client: AsyncIOMotorClient | None = None
```

This manager lazily instantiates the database connection pool the first time `get_database()` is invoked, keeping the startup profile light. The `mongodb_uri` value is supplied via the Pydantic variables defined in the system `settings.py`.

---

## Data Models

`model.py` creates the bridge between the standard `Message` objects (defined in `src/channel/base.py`) and the MongoDB BSON format.

### `DBMessage`

The schema strictly requires an `_id` field (which Maps to MongoDB's internal primary keys) and a `channel_type` string (e.g. `"discord"` or `"telegram"`).

```python
class DBMessage(BaseModel):
    id: Optional[Any] = Field(default=None, alias="_id")
    content: str
    sender_id: str
    timestamp: datetime
    metadata: Optional[dict] = None
    channel_type: str
```

A handy factory method `.from_channel_message()` is provided to instantly upgrade a standard transient message into a storable database document.

---

## Message Operations

`message.py` encapsulates common CRUD actions against the `messages` collection. 

It keeps the raw motor querying (like `collection.insert_one` or `collection.find`) siloed away from the rest of the app context, allowing other parts of the backend to read or write without knowing the implementation details of the underlying driver.
