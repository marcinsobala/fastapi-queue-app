from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from loguru import logger

from adapters.data_access_layer.currencies import (
    AbstractCurrenciesDAL,
    CurrencyAlreadyExists,
    ResourceDoesNotExist,
    # CurrencyIsUsedInTransfer,
)
from api.dependencies import get_currencies_dal
from models import currency as model


router = APIRouter()


@router.get("/{currency_id}")
async def get_currency(
    currency_id: int,
    currencies_dal: AbstractCurrenciesDAL = Depends(get_currencies_dal)
) -> model.Currency:
    try:
        return await currencies_dal.get_currency(currency_id)
    except ResourceDoesNotExist as ex:
        logger.exception(str(ex))
        raise HTTPException(404, str(ex))


@router.get("/")
async def get_all_currencies(
    acronym: str | None = Query(None, max_length=3),
    currencies_dal: AbstractCurrenciesDAL = Depends(get_currencies_dal),
):
    filters = {}
    if acronym is not None:
        filters["acronym"] = acronym
    return await currencies_dal.get_currencies(filters)


@router.post("/")
async def create_currency(
    currency: model.CurrencyIn,
    currencies_dal: AbstractCurrenciesDAL = Depends(get_currencies_dal),
) -> model.Currency:
    try:
        return await currencies_dal.create_currency(currency.dict())
    except CurrencyAlreadyExists as ex:
        logger.exception(str(ex))
        raise HTTPException(409, str(ex))


@router.patch("/{currency_id}")
async def update_currency(
    currency_id: int,
    currency_upd: model.CurrencyUpd,
    currencies_dal: AbstractCurrenciesDAL = Depends(get_currencies_dal),
) -> model.Currency:
    try:
        await currencies_dal.update_currency(currency_id, currency_upd.dict(exclude_unset=True))
    except ResourceDoesNotExist as ex:
        logger.exception(str(ex))
        raise HTTPException(404, str(ex))
    except CurrencyAlreadyExists as ex:
        logger.exception(str(ex))
        raise HTTPException(409, str(ex))

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
    # except CurrencyIsUsedInTransfer as ex:
    #     logger.exception(str(ex))
    #     raise HTTPException(403, str(ex))
    except ResourceDoesNotExist as ex:
        logger.exception(str(ex))
        raise HTTPException(404, str(ex))
