from entrypoints.api.endpoints import (
    currencies,
    transfers,
    users,
)
from fastapi import APIRouter

global_router = APIRouter()

global_router.include_router(
    currencies.router,
    prefix="/currencies",
    tags=["currencies"],
)
global_router.include_router(
    transfers.router,
    prefix="/transfers",
    tags=["transfers"],
)
global_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)
