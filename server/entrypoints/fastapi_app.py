from adapters.database import create_tables
from api.routing import global_router
from fastapi import FastAPI
from uvicorn import run


def create_app() -> FastAPI:
    fastapi_app = FastAPI()

    @fastapi_app.get("/")
    def home() -> str:
        return "Hello, worlds!"

    @fastapi_app.on_event("startup")
    def startup() -> None:
        create_tables()

    fastapi_app.include_router(global_router)
    return fastapi_app


app = create_app()

if __name__ == "__main__":
    run(
        "entrypoints.fastapi_app:app",
        host="0.0.0.0",
        port=8080,
    )
