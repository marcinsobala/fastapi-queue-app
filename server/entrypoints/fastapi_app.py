from fastapi import FastAPI
from uvicorn import run

from entrypoints.api.routing import global_router
from adapters.database import create_tables


def create_app():
    app = FastAPI()

    @app.get("/")
    def home():
        return "Hello, world!"

    @app.on_event("startup")
    async def startup():
        await create_tables()

    app.include_router(global_router)
    return app


app = create_app()

if __name__ == '__main__':
    run(
        "entrypoints.fastapi_app:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
