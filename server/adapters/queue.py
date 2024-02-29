from abc import (
    ABC,
    abstractmethod,
)

import config
from celery import Celery
from exceptions import WrongTaskParamsType
from models.tasks import (
    MsgLogger,
    TaskParams,
)

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
    "default_task": "default-queue",
}

param_types_by_task_name = {
    "default_task": MsgLogger,
}


class IQueueAdapter(ABC):
    app = celery_app

    @staticmethod
    def _validate_task_params(task_name: str, params: TaskParams) -> None:
        expected_type = param_types_by_task_name.get(task_name)
        if not isinstance(params, expected_type):
            raise WrongTaskParamsType(f"Expected {expected_type} as param type")

    @abstractmethod
    def add_task(self, queue_name: str, params: TaskParams) -> str:
        ...

    @abstractmethod
    def get_task_result(self, task_id: str) -> dict:
        ...


class QueueAdapter(IQueueAdapter):
    def add_task(self, task_name: str, params: TaskParams) -> str:
        self._validate_task_params(task_name, params)

        return self.app.send_task(
            task_name,
            kwargs=params.__dict__,
        ).id

    def get_task_result(self, task_id: str) -> dict:
        return self.app.AsyncResult(task_id).result
