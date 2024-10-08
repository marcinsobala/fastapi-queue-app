from abc import (
    ABC,
    abstractmethod,
)

from celery import Celery

from core import config
from core.exceptions import (
    TaskDoesNotExist,
    WrongTaskParamsType,
)
from models.tasks import (
    TaskParams,
    UrlShorten,
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

task_routes = {
    "shorten_url": "default-queue",
}
celery_app.conf.task_routes = task_routes

param_types_by_task_name = {
    "shorten_url": UrlShorten,
}


class IQueueAdapter(ABC):
    @staticmethod
    def _validate_task(task_name: str) -> None:
        if task_name not in param_types_by_task_name:
            raise TaskDoesNotExist(f"Task {task_name} does not exist")

    @staticmethod
    def _validate_task_params(task_name: str, params: TaskParams) -> None:
        expected_type = param_types_by_task_name.get(task_name)
        if not isinstance(params, expected_type):
            raise WrongTaskParamsType(f"Expected {expected_type} as param type")

    def add_task(self, task_name: str, params: TaskParams) -> str:
        self._validate_task(task_name)
        self._validate_task_params(task_name, params)

        return self._add_task(task_name, params)

    @abstractmethod
    def _add_task(self, task_name: str, params: TaskParams) -> str:
        ...

    @abstractmethod
    def get_task_result(self, task_id: str) -> dict:
        ...


class QueueAdapter(IQueueAdapter):
    def _add_task(self, task_name: str, params: TaskParams) -> str:
        return celery_app.send_task(
            task_name,
            kwargs=params.__dict__,
        ).id

    def get_task_result(self, task_id: str) -> dict:
        return celery_app.AsyncResult(task_id).result
