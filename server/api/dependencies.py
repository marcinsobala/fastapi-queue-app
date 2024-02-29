from contextlib import contextmanager

from adapters.database import session_factory
from adapters.repositories.currency import (
    CurrencyRepository,
    ICurrencyRepository,
)
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

# async def get_users_dal() -> AsyncGenerator[UsersDAL, None]:
#     async with async_session() as session:
#         async with session.begin():
#             yield UsersDAL(session)


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


# async def get_currencies_dal() -> AsyncGenerator[CurrencyRepository, None]:
#     async with async_session() as session:
#         async with session.begin():
#             yield CurrencyRepository(session)


# async def get_transfers_dal() -> AsyncGenerator[TransfersDAL, None]:
#     async with async_session() as session:
#         async with session.begin():
#             yield TransfersDAL(session)
