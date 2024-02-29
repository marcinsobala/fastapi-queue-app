from adapters.queue import celery_app


@celery_app.task(name="default_task")
def log_msg(msg: str) -> dict[str, str]:
    return {"msg": msg}
