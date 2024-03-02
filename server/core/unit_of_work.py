import abc
from collections.abc import Callable
from typing import Any

from sqlalchemy.orm.session import Session

from adapters.database import session_factory
from adapters.repositories.url import (
    IUrlRepository,
    UrlRepository,
)


class IUnitOfWork(abc.ABC):
    urls: IUrlRepository

    def __enter__(self) -> "IUnitOfWork":
        return self

    def __exit__(self, *args: Any) -> None:
        self.rollback()

    @abc.abstractmethod
    def commit(self) -> None:
        ...

    @abc.abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, sess_factory: Callable[[], Session] = session_factory) -> None:
        self.session_factory = sess_factory

    def __enter__(self) -> IUnitOfWork:
        self.session = self.session_factory()
        self.urls = UrlRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args: Any) -> None:
        super().__exit__(*args)
        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
