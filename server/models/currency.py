from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
)


class CurrencyIn(BaseModel):
    name: str
    acronym: str = Field(..., max_length=3)

    class Config:
        orm_mode = True


class Currency(CurrencyIn):
    id: PositiveInt


class CurrencyUpd(BaseModel):
    name: str | None
    acronym: str | None = Field(None, max_length=3)
