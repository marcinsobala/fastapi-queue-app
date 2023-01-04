from datetime import date, time
from decimal import Decimal

from pydantic import BaseModel, PositiveInt

from models.user import User
from models.currency import Currency


class TransferBase(BaseModel):
    amount: Decimal
    title: str
    day: date
    time: time


class TransferIn(TransferBase):
    currency_id: PositiveInt
    user_id: PositiveInt


class Transfer(TransferBase):
    id: PositiveInt
    currency: Currency
    user: User


class TransferUpd(BaseModel):
    amount: Decimal | None
    title: str | None
    day: date | None
    time: time | None
    currency_id: PositiveInt | None
    user_id: PositiveInt | None


class TransferQuery(TransferUpd):
    ...
