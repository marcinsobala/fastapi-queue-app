from uvicorn import run

if __name__ == "__main__":
    run(
        "entrypoints.fastapi_app:app",
        host="0.0.0.0",
        port=8090,
        reload=True,
    )
