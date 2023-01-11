from adapters.database import create_tables
from entrypoints.api.routing import global_router
from fastapi import FastAPI
from uvicorn import run


def create_app() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    def home() -> str:
        return "Hello, world!"

    @app.on_event("startup")
    async def startup() -> None:
        await create_tables()

    app.include_router(global_router)
    return app


app = create_app()

if __name__ == "__main__":
    run(
        "entrypoints.fastapi_app:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
    )
