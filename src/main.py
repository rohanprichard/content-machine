from server import app
import uvicorn
from settings import get_settings


settings = get_settings()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port
    )