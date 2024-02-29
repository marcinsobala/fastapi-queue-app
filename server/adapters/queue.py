from abc import (
    ABC,
    abstractmethod,
)

import config
from celery import Celery

celery_app = Celery(
    "worker",
    backend="redis://:{}@{}:{}/0".format(
        config.REDIS_PASSWORD,
        config.REDIS_SERVER,
        config.REDIS_PORT,
    ),
    broker="amqp://{}:{}@{}:{}//".format(
        config.RABBITMQ_USERNAME,
        config.RABBITMQ_PASSWORD,
        config.RABBITMQ_SERVER,
        config.RABBITMQ_PORT,
    ),
)

celery_app.conf.task_routes = {
    "entrypoints.worker.log_msg": "default-queue",
}


class IQueueAdapter(ABC):
    app = celery_app

    @abstractmethod
    def add_task(self, queue_name: str, *args: tuple, **kwargs: dict) -> str:
        ...

    @abstractmethod
    def get_task(self, task_id: str) -> dict:
        ...


class QueueAdapter(IQueueAdapter):
    def add_task(self, queue_name: str, *args: tuple, **kwargs: dict) -> str:
        return self.app.send_task(
            queue_name,
            kwargs=kwargs,
        ).id

    def get_task(self, task_id: str) -> dict:
        return self.app.AsyncResult(task_id).info
