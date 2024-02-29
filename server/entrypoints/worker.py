from adapters.queue import celery_app
from loguru import logger


@celery_app.task(name="dude_task")
def log_msg(msg: str) -> dict[str, str]:
    logger.info(msg)
    return {"msg": msg}
