from abc import (
    ABC,
    abstractmethod,
)
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
    def get_currency(self, currency_id: int):
        pass

    @abstractmethod
    def get_currencies(self, filters: dict[str, Any] | None = None):
        pass

    @abstractmethod
    def create_currency(self, create_data: dict[str, Any]):
        pass

    @abstractmethod
    def update_currency(self, currency_id: int, update_data: dict[str, Any]):
        pass

    @abstractmethod
    def delete_currency(self, currency_id: int):
        pass


class CurrenciesDAL(AbstractCurrenciesDAL):
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_currency(self, currency_id: int):
        currency = await self.session.get(CurrencyDb, currency_id)
        if currency is None:
            raise ResourceDoesNotExist
        return currency

    async def get_currencies(self, filters: dict[str, Any] | None = None):
        currencies = await self.session.execute(select(CurrencyDb).filter_by(**filters or {}))
        return currencies.scalars().all()

    async def create_currency(self, create_data: dict[str, Any]):
        new_currency = CurrencyDb(**create_data)
        try:
            self.session.add(new_currency)
            await self.session.flush()
        except IntegrityError:
            raise ResourceAlreadyExists
        return new_currency

    async def update_currency(self, currency_id: int, update_data: dict[str, Any]):
        currency = await self.get_currency(currency_id)
        try:
            for key, value in update_data.items():
                setattr(currency, key, value)
            await self.session.flush()
        except IntegrityError:
            raise ResourceAlreadyExists

    async def delete_currency(self, currency_id: int):
        q = delete(CurrencyDb).where(CurrencyDb.id == currency_id)
        try:
            delete_operation = await self.session.execute(q)
        except IntegrityError:
            raise CurrencyIsUsedInTransfer
        if delete_operation.rowcount == 0:
            raise ResourceDoesNotExist
