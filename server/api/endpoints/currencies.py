from adapters.repositories.currency import ICurrencyRepository
from api.dependencies import currency_repository
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
from models import currency as model

router = APIRouter()


@router.get(
    "/{currency_id}",
    response_model=model.Currency,
)
def get_currency(
    currency_id: int,
    repo: ICurrencyRepository = Depends(currency_repository),
) -> model.Currency:
    try:
        return model.Currency.from_orm(repo.get_currency(currency_id))
    except ResourceDoesNotExist:
        msg = f"Currency with id: {currency_id} does not exist"
        logger.exception(msg)
        raise HTTPException(404, msg)


@router.get(
    "/",
    response_model=list[model.Currency],
)
def get_all_currencies(
    query_params: model.CurrencyQuery = Depends(),
    repo: ICurrencyRepository = Depends(currency_repository),
) -> list[model.Currency]:
    filters = query_params.dict(exclude_none=True)
    return repo.get_currencies(filters)


@router.post(
    "/",
    response_model=model.Currency,
)
def create_currency(
    currency: model.CurrencyIn,
    repo: ICurrencyRepository = Depends(currency_repository),
) -> model.Currency:
    try:
        new_currency = repo.create_currency(currency.dict())
    except ResourceAlreadyExists:
        msg = f"Currency: {currency.acronym} already exists!"
        logger.exception(msg)
        raise HTTPException(409, msg)

    repo.session.commit()
    return model.Currency.from_orm(new_currency)


@router.patch(
    "/{currency_id}",
    response_model=model.Currency,
)
def update_currency(
    currency_id: int,
    currency_upd: model.CurrencyUpd,
    repo: ICurrencyRepository = Depends(currency_repository),
) -> model.Currency:
    try:
        repo.update_currency(currency_id, currency_upd.dict(exclude_unset=True))
    except ResourceDoesNotExist:
        msg = f"Currency with id {currency_id} not found"
        logger.exception(msg)
        raise HTTPException(404, msg)
    except ResourceAlreadyExists:
        msg = f"Currency with data: {currency_upd} already exists"
        logger.exception(msg)
        raise HTTPException(409, msg)

    repo.session.commit()
    return model.Currency.from_orm(repo.get_currency(currency_id))


@router.delete(
    "/{currency_id}",
    status_code=204,
)
def delete_currency(
    currency_id: int,
    repo: ICurrencyRepository = Depends(currency_repository),
) -> None:
    try:
        repo.delete_currency(currency_id)
    except ResourceDoesNotExist:
        msg = f"Currency with id {currency_id} not found"
        logger.exception(msg)
        raise HTTPException(404, msg)

    repo.session.commit()
