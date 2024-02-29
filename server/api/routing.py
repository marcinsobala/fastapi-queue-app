from api.endpoints import (
    currencies,
    task_test,
)
from fastapi import APIRouter

global_router = APIRouter()

global_router.include_router(
    currencies.router,
    prefix="/currencies",
    tags=["currencies"],
)
global_router.include_router(
    task_test.router,
    prefix="/task",
    tags=["task"],
)
