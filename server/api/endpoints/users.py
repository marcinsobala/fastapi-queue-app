from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from loguru import logger

from adapters.data_access_layer.users import (
    AbstractUsersDAL,
    ResourceDoesNotExist,
)
from exceptions import UserAlreadyExists
from api.dependencies import get_users_dal
from models import user as model


router = APIRouter()


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    users_dal: AbstractUsersDAL = Depends(get_users_dal)
) -> model.User:
    try:
        return await users_dal.get_user(user_id)
    except ResourceDoesNotExist as ex:
        logger.exception(str(ex))
        raise HTTPException(404, str(ex))
    
    
@router.get("/")
async def get_all_users(
    query_params: model.UserQuery = Depends(),
    users_dal: AbstractUsersDAL = Depends(get_users_dal)
) -> list[model.User]:
    filters = query_params.dict(exclude_none=True)
    return await users_dal.get_users(filters)


@router.post("/")
async def create_user(
    user: model.UserIn,
    users_dal: AbstractUsersDAL = Depends(get_users_dal),
) -> model.User:
    try:
        return await users_dal.create_user(user.dict())
    except UserAlreadyExists as ex:
        logger.exception(str(ex))
        raise HTTPException(409, str(ex))


@router.patch("/{user_id}")
async def update_user(
    user_id: int,
    user_upd: model.UserUpd,
    users_dal: AbstractUsersDAL = Depends(get_users_dal),
) -> model.User:
    try:
        await users_dal.update_user(user_id, user_upd.dict(exclude_unset=True))
    except ResourceDoesNotExist as ex:
        logger.exception(str(ex))
        raise HTTPException(404, str(ex))
    except UserAlreadyExists as ex:
        logger.exception(str(ex))
        raise HTTPException(409, str(ex))

    return await users_dal.get_user(user_id)


@router.delete(
    "/{user_id}",
    status_code=204,
)
async def delete_user(
    user_id: int,
    users_dal: AbstractUsersDAL = Depends(get_users_dal),
):
    try:
        await users_dal.delete_user(user_id)
    except ResourceDoesNotExist as ex:
        logger.exception(str(ex))
        raise HTTPException(404, str(ex))

