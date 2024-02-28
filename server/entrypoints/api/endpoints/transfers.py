from adapters.database import (
    CurrencyDb,
    UserDb,
)
from adapters.repositories.currency import ICurrencyRepository
from adapters.repositories.transfers import AbstractTransfersDAL
from adapters.repositories.users import AbstractUsersDAL
from entrypoints.api.dependencies import (
    get_currencies_dal,
    get_transfers_dal,
    get_users_dal,
)
from exceptions import (
    CurrencyOrUserDoesNotExist,
    ResourceDoesNotExist,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from loguru import logger
from models import transfer as model

router = APIRouter()


async def _get_currency(
    currency_id: int,
    currencies_dal: ICurrencyRepository,
) -> CurrencyDb:
    try:
        return await currencies_dal.get_currency(currency_id)
    except ResourceDoesNotExist:
        msg = f"Currency with id: {currency_id} not found"
        logger.exception(msg)
        raise HTTPException(404, msg)


async def _get_user(
    user_id: int,
    users_dal: AbstractUsersDAL,
) -> UserDb:
    try:
        return await users_dal.get_user(user_id)
    except ResourceDoesNotExist:
        msg = f"User with id {user_id} not found"
        logger.error(msg)
        raise HTTPException(404, msg)


@router.get(
    "/{transfer_id}",
    response_model=model.TransferDetail,
)
async def get(
    transfer_id: int,
    currencies_dal: ICurrencyRepository = Depends(get_currencies_dal),
    transfers_dal: AbstractTransfersDAL = Depends(get_transfers_dal),
    users_dal: AbstractUsersDAL = Depends(get_users_dal),
) -> model.TransferDetail:
    try:
        transfer_db = await transfers_dal.get_transfer(transfer_id)
    except ResourceDoesNotExist:
        msg = f"Transfer with id: {transfer_id} not found"
        logger.exception(msg)
        raise HTTPException(404, msg)

    return model.TransferDetail(
        **transfer_db.__dict__,
        currency=await _get_currency(transfer_db.currency_id, currencies_dal),
        user=await _get_user(transfer_db.user_id, users_dal),
    )


@router.get(
    "/",
    response_model=list[model.Transfer],
)
async def get_all_transfers(
    query_params: model.TransferQuery = Depends(),
    transfers_dal: AbstractTransfersDAL = Depends(get_transfers_dal),
) -> list[model.Transfer]:
    filters = query_params.dict(exclude_none=True)
    return await transfers_dal.get_transfers(filters)


@router.post(
    "/",
    response_model=model.Transfer,
)
async def create_transfer(
    transfer: model.TransferIn,
    currencies_dal: ICurrencyRepository = Depends(get_currencies_dal),
    transfers_dal: AbstractTransfersDAL = Depends(get_transfers_dal),
    users_dal: AbstractUsersDAL = Depends(get_users_dal),
) -> model.Transfer:
    await _get_currency(transfer.currency_id, currencies_dal)
    await _get_user(transfer.user_id, users_dal)
    return await transfers_dal.create_transfer(transfer.dict())


@router.patch(
    "/{transfer_id}",
    response_model=model.Transfer,
)
async def update_transfer(
    transfer_id: int,
    transfer_upd: model.TransferUpd,
    transfers_dal: AbstractTransfersDAL = Depends(get_transfers_dal),
) -> model.Transfer:
    try:
        await transfers_dal.update_transfer(transfer_id, transfer_upd.dict(exclude_unset=True))
    except ResourceDoesNotExist:
        msg = f"Transfer with id: {transfer_id} not found"
        logger.exception(msg)
        raise HTTPException(404, msg)
    except CurrencyOrUserDoesNotExist:
        msg = "Provided currency or user do not exist"
        logger.exception(msg)
        raise HTTPException(404, msg)

    return await transfers_dal.get_transfer(transfer_id)


@router.delete(
    "/{transfer_id}",
    status_code=204,
)
async def delete_transfer(
    transfer_id: int,
    transfers_dal: AbstractTransfersDAL = Depends(get_transfers_dal),
) -> None:
    try:
        return await transfers_dal.delete_transfer(transfer_id)
    except ResourceDoesNotExist:
        msg = f"Transfer with id: {transfer_id} not found"
        logger.exception(msg)
        raise HTTPException(404, msg)
