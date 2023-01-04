from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from loguru import logger


from api.dependencies import (
    get_users_dal,
    get_currencies_dal,
    get_transfers_dal
)
from adapters.data_access_layer.users import AbstractUsersDAL
from adapters.data_access_layer.currencies import AbstractCurrenciesDAL
from adapters.data_access_layer.transfers import AbstractTransfersDAL
from exceptions import TransferAlreadyExists, ResourceDoesNotExist
from models import transfer as model

router = APIRouter()


async def _get_currency_exists(currency_id: int):
    dal = await anext(get_currencies_dal())
    try:
        await dal.get_currency(currency_id)
    except ResourceDoesNotExist as ex:
        logger.exception(str(ex))
        raise HTTPException(404, str(ex))


@router.get("/{transfer_id}")
async def get(
    transfer_id: int,
    transfers_dal: AbstractTransfersDAL = Depends(get_transfers_dal),
) -> model.Transfer:
    try:
        return await transfers_dal.get_transfer(transfer_id)
    except ResourceDoesNotExist as ex:
        logger.exception(str(ex))
        raise HTTPException(404, str(ex))


@router.get("/")
async def get_all(
    query_params: model.TransferQuery = Depends(),
    transfers_dal: AbstractTransfersDAL = Depends(get_transfers_dal)
) -> list[model.Transfer]:
    filters = query_params.dict(exclude_none=True)
    return await transfers_dal.get_transfers(filters)


@router.post("/")
async def create_transfer(
    transfer: model.TransferIn,
    transfers_dal: AbstractTransfersDAL = Depends(get_transfers_dal),
) -> model.Transfer:
    currency = await _get_currency_exists(transfer.currency_id)

    try:
        return await transfers_dal.create_transfer(transfer.dict())
    except ResourceDoesNotExist as ex:
        logger.exception(str(ex), 404)
        raise HTTPException(404, str(ex))


@router.patch("/{transfer_id}")
async def update_transfer(
    transfer_id: int,
    transfer_upd: model.TransferUpd,
    transfers_dal: AbstractTransfersDAL = Depends(get_transfers_dal),
) -> model.Transfer:
    try:
        await transfers_dal.update_transfer(transfer_id, transfer_upd.dict(exclude_unset=True))
    except ResourceDoesNotExist as ex:
        logger.exception(str(ex), 404)
        raise HTTPException(404, str(ex))
    
    return await transfers_dal.get_transfer(transfer_id)


@router.delete(
    "/{transfer_id}",
    status_code=204,
)
async def delete_transfer(
    transfer_id: int,
    transfers_dal: AbstractTransfersDAL = Depends(get_transfers_dal),
):
    try:
        return await transfers_dal.delete_transfer(transfer_id)
    except ResourceDoesNotExist as ex:
        logger.exception(str(ex), 404)
        raise HTTPException(404, str(ex))