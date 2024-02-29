from contextlib import contextmanager

from adapters.database import session_factory
from adapters.queue import (
    IQueueAdapter,
    QueueAdapter,
)
from adapters.repositories.currency import (
    CurrencyRepository,
    ICurrencyRepository,
)
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


@contextmanager
def uow() -> Session:
    session = session_factory()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(500, str(e))
    finally:
        session.close()


def currency_repository() -> ICurrencyRepository:
    with uow() as db_session:
        yield CurrencyRepository(db_session=db_session)


def queue_adapter() -> IQueueAdapter:
    return QueueAdapter()
