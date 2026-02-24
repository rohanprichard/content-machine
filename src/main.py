import uvicorn
from src.server import app
from src.settings import get_settings


settings = get_settings()


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )
