import uvicorn
from fastapi import FastAPI

from app.api.endpoints import api_router
from app.resource.database import create_session_manager
from settings import Settings


def create_app(config: Settings) -> FastAPI:
    app = FastAPI()
    app.include_router(api_router, prefix="/api/v1", tags=["api"])
    session_factory = create_session_manager(config)
    app.state.session_factory = session_factory
    return app


if __name__ == "__main__":
    app = create_app(Settings())
    uvicorn.run(app, host="localhost", port=5000, log_level="info")
