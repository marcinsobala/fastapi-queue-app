from contextlib import nullcontext as does_not_raise

import pytest

from adapters.queue import (
    IQueueAdapter,
    task_routes,
)
from core.exceptions import (
    TaskDoesNotExist,
    WrongTaskParamsType,
)
from models.tasks import (
    TaskParams,
    UrlShorten,
)


def test_validates_task_params() -> None:
    with does_not_raise():
        IQueueAdapter._validate_task_params("shorten_url", UrlShorten(url="http://example.com"))


def test_raises_wrong_task_params_type() -> None:
    class WrongTaskParams(TaskParams):
        pass

    with pytest.raises(WrongTaskParamsType):
        IQueueAdapter._validate_task_params("shorten_url", WrongTaskParams())


def test_raises_task_does_not_exist() -> None:
    with pytest.raises(TaskDoesNotExist):
        IQueueAdapter._validate_task("non_existent_task")


def test_validates_task_exists() -> None:
    with does_not_raise():
        for key in task_routes:
            IQueueAdapter._validate_task(key)
