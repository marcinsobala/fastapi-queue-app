from adapters.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
)


class CurrencyDb(Base):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(length=30), nullable=False)
    acronym = Column(String(length=3), nullable=False, unique=True)
