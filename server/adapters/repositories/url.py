from abc import (
    ABC,
    abstractmethod,
)
from typing import Any

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.exceptions import (
    ResourceAlreadyExists,
    ResourceDoesNotExist,
)
from schemas.url import UrlDb


class IUrlRepository(ABC):
    session: Session

    @abstractmethod
    def get_by_url(self, url: str) -> type[UrlDb]:
        pass

    @abstractmethod
    def get_by_short_url(self, short_url: str) -> type[UrlDb]:
        pass

    @abstractmethod
    def get_all(self) -> list[type[UrlDb]]:
        pass

    # @abstractmethod
    # def get_currencies(
    #     self,
    #     filters: dict[str, Any] | None = None,
    # ) -> list[UrlDb]:
    #     pass

    @abstractmethod
    def create(self, create_data: dict[str, Any]) -> type[UrlDb]:
        pass

    @abstractmethod
    def update_with_short_url(
        self,
        url: str,
        short_url: str,
    ) -> None:
        pass

    @abstractmethod
    def delete(self, url_id: int) -> None:
        pass


class UrlRepository(IUrlRepository):
    def __init__(self, db_session: Session):
        self.session = db_session

    def get_by_url(self, url: str) -> type[UrlDb]:
        url_db = self.session.query(UrlDb).filter_by(url=url).first()
        if url_db is None:
            raise ResourceDoesNotExist
        return url_db

    def get_by_short_url(self, short_url: str) -> type[UrlDb]:
        url = self.session.query(UrlDb).filter_by(short_url=short_url).first()
        if url is None:
            raise ResourceDoesNotExist
        return url

    def get_all(self) -> list[type[UrlDb]]:
        return self.session.query(UrlDb).all()

    def create(self, create_data: dict[str, Any]) -> None:
        new_url = UrlDb(**create_data)
        try:
            self.session.add(new_url)
            self.session.flush()
        except IntegrityError:
            raise ResourceAlreadyExists

    def update_with_short_url(
        self,
        url: str,
        short_url: str,
    ) -> None:
        q = self.session.query(UrlDb).filter(UrlDb.url == url).update({"short_url": short_url})

        if q == 0:
            raise ResourceDoesNotExist

    def delete(self, url_id: int) -> None:
        q = delete(UrlDb).where(UrlDb.id == url_id)
        delete_operation = self.session.execute(q)
        if delete_operation.rowcount == 0:
            raise ResourceDoesNotExist
