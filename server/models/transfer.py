from datetime import date, time
from decimal import Decimal

from pydantic import BaseModel, PositiveInt


class TransferIn(BaseModel):
    amount: Decimal
    title: str
    day: date
    time: time
    currency_id: PositiveInt
    user_id: PositiveInt

    class Config:
        orm_mode = True


class Transfer(TransferIn):
    id: PositiveInt


class TransferUpd(BaseModel):
    amount: Decimal | None
    title: str | None
    day: date | None
    time: time | None
    currency_id: PositiveInt | None
    user_id: PositiveInt | None
