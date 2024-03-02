from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    text,
)

from adapters.database import Base


class UrlDb(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    url = Column(String, nullable=False, index=True, unique=True)
    short_url = Column(String, nullable=True, index=True)
