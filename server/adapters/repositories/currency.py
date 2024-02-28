from abc import (
    ABC,
    abstractmethod,
)
from typing import Any

from exceptions import (
    CurrencyIsUsedInTransfer,
    ResourceAlreadyExists,
    ResourceDoesNotExist,
)
from schemas.currency import CurrencyDb
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class ICurrencyRepository(ABC):
    session: Session

    @abstractmethod
    def get_currency(self, currency_id: int) -> type[CurrencyDb]:
        pass

    @abstractmethod
    def get_currencies(
        self,
        filters: dict[str, Any] | None = None,
    ) -> list[CurrencyDb]:
        pass

    @abstractmethod
    def create_currency(self, create_data: dict[str, Any]) -> type[CurrencyDb]:
        pass

    @abstractmethod
    def update_currency(
        self,
        currency_id: int,
        update_data: dict[str, Any],
    ) -> None:
        pass

    @abstractmethod
    def delete_currency(self, currency_id: int) -> None:
        pass


class CurrencyRepository(ICurrencyRepository):
    def __init__(self, db_session: Session):
        self.session = db_session

    def get_currency(self, currency_id: int) -> type[CurrencyDb]:
        currency = self.session.get(CurrencyDb, currency_id)
        if currency is None:
            raise ResourceDoesNotExist
        return currency

    def get_currencies(self, filters: dict[str, Any] | None = None) -> list[type[CurrencyDb]]:
        return self.session.query(CurrencyDb).filter_by(**filters or {}).all()

    def create_currency(self, create_data: dict[str, Any]) -> CurrencyDb:
        new_currency = CurrencyDb(**create_data)
        try:
            self.session.add(new_currency)
            self.session.flush()
        except IntegrityError:
            raise ResourceAlreadyExists
        return new_currency

    def update_currency(self, currency_id: int, update_data: dict[str, Any]) -> None:
        currency = self.get_currency(currency_id)
        try:
            for key, value in update_data.items():
                setattr(currency, key, value)
            self.session.flush()
        except IntegrityError:
            raise ResourceAlreadyExists

    def delete_currency(self, currency_id: int) -> None:
        q = delete(CurrencyDb).where(CurrencyDb.id == currency_id)
        try:
            delete_operation = self.session.execute(q)
        except IntegrityError:
            raise CurrencyIsUsedInTransfer
        if delete_operation.rowcount == 0:
            raise ResourceDoesNotExist
