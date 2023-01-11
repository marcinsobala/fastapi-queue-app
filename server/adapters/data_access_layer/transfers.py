from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import Coroutine
from typing import Any

from adapters.database import TransferDb
from exceptions import (
    CurrencyOrUserDoesNotExist,
    ResourceDoesNotExist,
)
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class AbstractTransfersDAL(ABC):
    @abstractmethod
    def get_transfer(self, transfer_id: int) -> TransferDb:
        pass

    @abstractmethod
    def get_transfers(
        self,
        filters: dict[str, Any] | None = None,
    ) -> Coroutine[Any, Any, list[Any]] | list[TransferDb]:
        pass

    @abstractmethod
    def create_transfer(self, create_data: dict[str, Any]) -> TransferDb:
        pass

    @abstractmethod
    def update_transfer(
        self,
        transfer_id: int,
        update_data: dict[str, Any],
    ) -> Coroutine[Any, Any, None] | None:
        pass

    @abstractmethod
    def delete_transfer(self, transfer_id: int) -> Coroutine[Any, Any, None] | None:
        pass


class TransfersDAL(AbstractTransfersDAL):
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_transfer(self, transfer_id: int) -> TransferDb:
        transfer = await self.session.get(TransferDb, transfer_id)
        if transfer is None:
            raise ResourceDoesNotExist
        return transfer

    async def get_transfers(self, filters: dict[str, Any] | None = None) -> list[TransferDb]:
        transfers = await self.session.execute(select(TransferDb).filter_by(**filters or {}))
        return transfers.scalars().all()

    async def create_transfer(self, create_data: dict[str, Any]) -> TransferDb:
        new_transfer = TransferDb(**create_data)
        self.session.add(new_transfer)
        await self.session.flush()
        return new_transfer

    async def update_transfer(self, transfer_id: int, update_data: dict[str, Any]) -> None:
        transfer = await self.get_transfer(transfer_id)
        try:
            for key, value in update_data.items():
                setattr(transfer, key, value)
            await self.session.flush()
        except IntegrityError:
            raise CurrencyOrUserDoesNotExist

    async def delete_transfer(self, transfer_id: int) -> None:
        q = delete(TransferDb).where(TransferDb.id == transfer_id)
        delete_operation = await self.session.execute(q)
        if delete_operation.rowcount == 0:
            raise ResourceDoesNotExist
