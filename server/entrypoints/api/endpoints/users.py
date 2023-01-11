from adapters.data_access_layer.users import AbstractUsersDAL
from entrypoints.api.dependencies import get_users_dal
from exceptions import (
    ResourceAlreadyExists,
    ResourceDoesNotExist,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from loguru import logger
from models import user as model

router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=model.User,
)
async def get_user(
    user_id: int,
    users_dal: AbstractUsersDAL = Depends(get_users_dal),
) -> model.User:
    try:
        return await users_dal.get_user(user_id)
    except ResourceDoesNotExist:
        msg = f"User with id: {user_id} does not exist"
        logger.exception(msg)
        raise HTTPException(404, msg)


@router.get(
    "/",
    response_model=list[model.User],
)
async def get_all_users(
    query_params: model.UserQuery = Depends(),
    users_dal: AbstractUsersDAL = Depends(get_users_dal),
) -> list[model.User]:
    filters = query_params.dict(exclude_none=True)
    return await users_dal.get_users(filters)


@router.post(
    "/",
    response_model=model.User,
)
async def create_user(
    user: model.UserIn,
    users_dal: AbstractUsersDAL = Depends(get_users_dal),
) -> model.User:
    try:
        return await users_dal.create_user(user.dict())
    except ResourceAlreadyExists:
        msg = f"User with email: {user.email} already exists!"
        logger.exception(msg)
        raise HTTPException(409, msg)


@router.patch(
    "/{user_id}",
    response_model=model.User,
)
async def update_user(
    user_id: int,
    user_upd: model.UserUpd,
    users_dal: AbstractUsersDAL = Depends(get_users_dal),
) -> model.User:
    try:
        await users_dal.update_user(user_id, user_upd.dict(exclude_unset=True))
    except ResourceDoesNotExist:
        msg = f"User with id: {user_id} does not exist"
        logger.exception(msg)
        raise HTTPException(404, msg)
    except ResourceAlreadyExists:
        msg = f"User with following data: {user_upd} already exists!"
        logger.exception(msg)
        raise HTTPException(409, msg)

    return await users_dal.get_user(user_id)


@router.delete(
    "/{user_id}",
    status_code=204,
)
async def delete_user(
    user_id: int,
    users_dal: AbstractUsersDAL = Depends(get_users_dal),
) -> None:
    try:
        await users_dal.delete_user(user_id)
    except ResourceDoesNotExist:
        msg = f"User with id {user_id} not found"
        logger.exception(msg)
        raise HTTPException(404, msg)
