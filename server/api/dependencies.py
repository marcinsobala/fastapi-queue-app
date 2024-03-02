from adapters.queue import (
    IQueueAdapter,
    QueueAdapter,
)
from core.unit_of_work import (
    IUnitOfWork,
    SqlAlchemyUnitOfWork,
)


def unit_of_work() -> IUnitOfWork:
    return SqlAlchemyUnitOfWork()


def queue_adapter() -> IQueueAdapter:
    return QueueAdapter()
