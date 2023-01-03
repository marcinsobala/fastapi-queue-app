from abc import ABC, abstractmethod
from typing import (
    Any,
)

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from adapters.database import CurrencyDb


class CurrencyAlreadyExists(Exception):
    pass


class ResourceDoesNotExist(Exception):
    pass


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
            raise ResourceDoesNotExist(f"Currency with id: {currency_id} not found")
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
            raise CurrencyAlreadyExists(f"Currency: {new_currency.acronym} already exists!")
        return new_currency

    async def update_currency(self, currency_id: int, update_data: dict[str, Any]):
        currency = await self.get_currency(currency_id)
        try:
            for key, value in update_data.items():
                setattr(currency, key, value)
            await self.session.flush()
        except IntegrityError:
            raise CurrencyAlreadyExists(f"Currency with data: {update_data} already exists")

    async def delete_currency(self, currency_id: int):
        # forbid if currency is used in transfer

        q = delete(CurrencyDb).where(CurrencyDb.id == currency_id)
        delete_operation = await self.session.execute(q)
        if delete_operation.rowcount is 0:
            raise ResourceDoesNotExist(f"User with id {currency_id} not found")
