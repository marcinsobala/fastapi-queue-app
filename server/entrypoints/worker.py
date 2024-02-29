from loguru import logger


def log_msg(msg: str) -> None:
    logger.info(msg)
