import config
from sqlalchemy import (  # DECIMAL,; TIMESTAMP,; Boolean,; ForeignKey,; Column,; Integer,; String,
    create_engine,
)
from sqlalchemy.orm import (
    Session,
    declarative_base,
    sessionmaker,
)

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)


def session_factory() -> Session:
    return sessionmaker(bind=engine)()


Base = declarative_base()


# class UserDb(Base):
#     __tablename__ = "users"
#
#     id = Column(Integer, primary_key=True, nullable=False)
#     name = Column(String(), nullable=False)
#     email = Column(String(), nullable=False, unique=True)
#     surname = Column(String(), nullable=False)
#     premium = Column(Boolean(), nullable=False, default=False)
#
#
# class TransferDb(Base):
#     __tablename__ = "transfers"
#
#     id = Column(Integer, primary_key=True, nullable=False)
#     amount = Column(DECIMAL(), nullable=False)
#     title = Column(String(length=85), nullable=False)
#     timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
#     currency_id = Column(Integer, ForeignKey("currency.id"))
#     user_id = Column(Integer, ForeignKey("users.id"))


def create_tables() -> None:
    Base.metadata.create_all(engine)
