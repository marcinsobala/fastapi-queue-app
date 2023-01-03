from typing import AsyncGenerator


from adapters.database import async_session

from adapters.data_access_layer.currencies import CurrenciesDAL
from adapters.data_access_layer.users import UsersDAL


async def get_users_dal() -> AsyncGenerator[UsersDAL, None]:
    async with async_session() as session:
        async with session.begin():
            yield UsersDAL(session)


async def get_currencies_dal() -> AsyncGenerator[CurrenciesDAL, None]:
    async with async_session() as session:
        async with session.begin():
            yield CurrenciesDAL(session)