from fastapi import APIRouter

from api.endpoints import urls

global_router = APIRouter()

global_router.include_router(
    urls.router,
    tags=["urls"],
)
