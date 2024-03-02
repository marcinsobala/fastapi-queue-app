from datetime import datetime

from pydantic import (
    BaseModel,
    PositiveInt,
)


class UrlIn(BaseModel):
    url: str

    class Config:
        orm_mode = True


class Url(UrlIn):
    id: PositiveInt
    created_at: datetime
    short_url: str | None
