from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import Coroutine
from typing import Any

from adapters.database import CurrencyDb
from exceptions import (
    CurrencyIsUsedInTransfer,
    ResourceAlreadyExists,
    ResourceDoesNotExist,
)
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class AbstractCurrenciesDAL(ABC):
    @abstractmethod
    def get_currency(self, currency_id: int) -> CurrencyDb:
        pass

    @abstractmethod
    def get_currencies(
        self,
        filters: dict[str, Any] | None = None,
    ) -> Coroutine[Any, Any, list[Any]] | list[CurrencyDb]:
        pass

    @abstractmethod
    def create_currency(self, create_data: dict[str, Any]) -> CurrencyDb:
        pass

    @abstractmethod
    def update_currency(
        self,
        currency_id: int,
        update_data: dict[str, Any],
    ) -> Coroutine[Any, Any, None] | None:
        pass

    @abstractmethod
    def delete_currency(self, currency_id: int) -> Coroutine[Any, Any, None] | None:
        pass


class CurrenciesDAL(AbstractCurrenciesDAL):
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_currency(self, currency_id: int) -> CurrencyDb:
        currency = await self.session.get(CurrencyDb, currency_id)
        if currency is None:
            raise ResourceDoesNotExist
        return currency

    async def get_currencies(self, filters: dict[str, Any] | None = None) -> list[CurrencyDb]:
        currencies = await self.session.execute(select(CurrencyDb).filter_by(**filters or {}))
        return currencies.scalars().all()

    async def create_currency(self, create_data: dict[str, Any]) -> CurrencyDb:
        new_currency = CurrencyDb(**create_data)
        try:
            self.session.add(new_currency)
            await self.session.flush()
        except IntegrityError:
            raise ResourceAlreadyExists
        return new_currency

    async def update_currency(self, currency_id: int, update_data: dict[str, Any]) -> None:
        currency = await self.get_currency(currency_id)
        try:
            for key, value in update_data.items():
                setattr(currency, key, value)
            await self.session.flush()
        except IntegrityError:
            raise ResourceAlreadyExists

    async def delete_currency(self, currency_id: int) -> None:
        q = delete(CurrencyDb).where(CurrencyDb.id == currency_id)
        try:
            delete_operation = await self.session.execute(q)
        except IntegrityError:
            raise CurrencyIsUsedInTransfer
        if delete_operation.rowcount == 0:
            raise ResourceDoesNotExist
