from adapters.data_access_layer.currencies import AbstractCurrenciesDAL
from entrypoints.api.dependencies import get_currencies_dal
from exceptions import (
    CurrencyIsUsedInTransfer,
    ResourceAlreadyExists,
    ResourceDoesNotExist,
)
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from loguru import logger
from models import currency as model

router = APIRouter()


@router.get("/{currency_id}")
async def get_currency(
    currency_id: int,
    currencies_dal: AbstractCurrenciesDAL = Depends(get_currencies_dal),
) -> model.Currency:
    try:
        return await currencies_dal.get_currency(currency_id)
    except ResourceDoesNotExist as ex:
        logger.exception(str(ex))
        raise HTTPException(404, str(ex))


@router.get("/")
async def get_all_currencies(
    query_params: model.CurrencyQuery = Depends(),
    currencies_dal: AbstractCurrenciesDAL = Depends(get_currencies_dal),
):
    filters = query_params.dict(exclude_none=True)
    return await currencies_dal.get_currencies(filters)


@router.post("/")
async def create_currency(
    currency: model.CurrencyIn,
    currencies_dal: AbstractCurrenciesDAL = Depends(get_currencies_dal),
) -> model.Currency:
    try:
        return await currencies_dal.create_currency(currency.dict())
    except ResourceAlreadyExists:
        msg = f"Currency: {currency.acronym} already exists!"
        logger.exception(msg)
        raise HTTPException(409, msg)


@router.patch("/{currency_id}")
async def update_currency(
    currency_id: int,
    currency_upd: model.CurrencyUpd,
    currencies_dal: AbstractCurrenciesDAL = Depends(get_currencies_dal),
) -> model.Currency:
    try:
        await currencies_dal.update_currency(currency_id, currency_upd.dict(exclude_unset=True))
    except ResourceDoesNotExist:
        msg = f"Currency with id {currency_id} not found"
        logger.exception(msg)
        raise HTTPException(404, msg)
    except ResourceAlreadyExists:
        msg = f"Currency with data: {currency_upd} already exists"
        logger.exception(msg)
        raise HTTPException(409, msg)

    return await currencies_dal.get_currency(currency_id)


@router.delete(
    "/{currency_id}",
    status_code=204,
)
async def delete_currency(
    currency_id: int,
    currencies_dal: AbstractCurrenciesDAL = Depends(get_currencies_dal),
):
    try:
        await currencies_dal.delete_currency(currency_id)
    except CurrencyIsUsedInTransfer:
        msg = f"Cannot delete currency with id: {currency_id} as it is used in existing transfers."
        logger.exception(msg)
        raise HTTPException(403, msg)
    except ResourceDoesNotExist:
        msg = f"Currency with id {currency_id} not found"
        logger.exception(msg)
        raise HTTPException(404, msg)
