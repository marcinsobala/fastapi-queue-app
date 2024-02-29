from adapters.queue import IQueueAdapter
from api.dependencies import queue_adapter
from fastapi import (
    APIRouter,
    Depends,
)

router = APIRouter()


@router.get("/")
def get_task(
    task_id: str,
    queue: IQueueAdapter = Depends(queue_adapter),
) -> dict | None:
    task_result = queue.get_task_result(task_id)
    return task_result


@router.post("/")
def schedule_task(
    queue: IQueueAdapter = Depends(queue_adapter),
) -> str:
    task_id = queue.add_task("dude_task", msg="Hello, World!")
    return task_id
