from pydantic import (
    BaseModel,
    PositiveInt,
)


class UserIn(BaseModel):
    name: str
    surname: str
    email: str
    premium: bool | None = False

    class Config:
        orm_mode = True


class User(UserIn):
    id: PositiveInt


class UserUpd(BaseModel):
    name: str | None
    surname: str | None
    premium: bool | None
    email: str | None


class UserQuery(UserUpd):
    ...
