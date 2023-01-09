from datetime import datetime
from decimal import Decimal

from models.currency import Currency
from models.user import User
from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
)


class TransferBase(BaseModel):
    amount: Decimal
    title: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TransferIn(TransferBase):
    currency_id: PositiveInt
    user_id: PositiveInt


class Transfer(TransferIn):
    id: PositiveInt

    class Config:
        orm_mode = True


class TransferDetail(TransferBase):
    id: PositiveInt
    currency: Currency
    user: User


class TransferUpd(BaseModel):
    amount: Decimal | None
    title: str | None
    currency_id: PositiveInt | None
    user_id: PositiveInt | None


class TransferQuery(TransferUpd):
    ...
