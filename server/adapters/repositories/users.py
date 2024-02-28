from abc import (
    ABC,
    abstractmethod,
)
from collections.abc import Coroutine
from typing import Any

from adapters.database import (
    TransferDb,
    UserDb,
)
from exceptions import (
    ResourceAlreadyExists,
    ResourceDoesNotExist,
)
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class AbstractUsersDAL(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> UserDb:
        pass

    @abstractmethod
    def get_users(
        self,
        filters: dict[str, Any] | None = None,
    ) -> Coroutine[Any, Any, list[Any]] | list[UserDb]:
        pass

    @abstractmethod
    def create_user(self, create_data: dict[str, Any]) -> UserDb:
        pass

    @abstractmethod
    def update_user(
        self,
        user_id: int,
        update_data: dict[str, Any],
    ) -> Coroutine[Any, Any, None] | None:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> Coroutine[Any, Any, None] | None:
        pass


class UsersDAL(AbstractUsersDAL):
    def __init__(self, db_session: AsyncSession):
        self.session = db_session

    async def get_user(self, user_id: int) -> UserDb:
        user = await self.session.get(UserDb, user_id)
        if user is None:
            raise ResourceDoesNotExist
        return user

    async def get_users(self, filters: dict[str, Any] | None = None) -> list[UserDb]:
        users = await self.session.execute(select(UserDb).filter_by(**filters or {}))
        return users.scalars().all()

    async def create_user(self, create_data: dict[str, Any]) -> UserDb:
        new_user = UserDb(**create_data)
        try:
            self.session.add(new_user)
            await self.session.flush()
        except IntegrityError:
            raise ResourceAlreadyExists
        return new_user

    async def update_user(self, user_id: int, update_data: dict[str, Any]) -> None:
        user = await self.get_user(user_id)
        try:
            for key, value in update_data.items():
                setattr(user, key, value)
            await self.session.flush()
        except IntegrityError:
            raise ResourceAlreadyExists

    async def delete_user(self, user_id: int) -> None:
        await self.session.execute(delete(TransferDb).where(TransferDb.user_id == user_id))
        result = await self.session.execute(delete(UserDb).where(UserDb.id == user_id))
        if result.rowcount == 0:
            raise ResourceDoesNotExist
