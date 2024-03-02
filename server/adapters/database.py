from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    declarative_base,
    sessionmaker,
)

from core import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)


def session_factory() -> Session:
    return sessionmaker(bind=engine)()


Base = declarative_base()


def create_tables() -> None:
    Base.metadata.create_all(engine)
