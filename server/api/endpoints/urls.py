from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from fastapi.responses import RedirectResponse
from loguru import logger

from adapters.queue import IQueueAdapter
from api.dependencies import (
    queue_adapter,
    unit_of_work,
)
from core.exceptions import (
    ResourceAlreadyExists,
    ResourceDoesNotExist,
)
from core.unit_of_work import IUnitOfWork
from models import url as model
from models.tasks import UrlShorten

router = APIRouter()


@router.get(
    "/",
    response_model=model.Url,
    responses={404: {"description": "Url does not exist!"}},
)
def get_url(
    url: str = Query(...),
    uow: IUnitOfWork = Depends(unit_of_work),
) -> model.Url:
    with uow:
        try:
            return model.Url.from_orm(uow.urls.get_by_url(url))
        except ResourceDoesNotExist:
            msg = f"Url: {url} does not exist!"
            logger.exception(msg)
            raise HTTPException(404, msg)


@router.get(
    "/short_url",
    response_model=model.Url,
    responses={404: {"description": "Short URL does not exist!"}},
)
def get_url_by_short_url(
    short_url: str = Query(...),
    uow: IUnitOfWork = Depends(unit_of_work),
) -> model.Url:
    with uow:
        try:
            db_url = uow.urls.get_by_short_url(short_url)
        except ResourceDoesNotExist:
            msg = f"Short URL: {short_url} does not exist!"
            logger.error(msg)
            raise HTTPException(404, msg)

        return model.Url.from_orm(db_url)


@router.get(
    "/all",
    response_model=list[model.Url],
)
def get_all_urls(
    uow: IUnitOfWork = Depends(unit_of_work),
) -> list[model.Url]:
    with uow:
        return [model.Url.from_orm(url) for url in uow.urls.get_all()]


@router.post(
    "/",
    status_code=201,
    responses={409: {"description": "Url already exists!"}},
)
def create_shortened_url(
    body: model.UrlIn,
    uow: IUnitOfWork = Depends(unit_of_work),
    q_adapter: IQueueAdapter = Depends(queue_adapter),
) -> str:
    with uow:
        try:
            uow.urls.create(body.dict())
        except ResourceAlreadyExists:
            msg = f"Url: {body.url} already exists!"
            logger.error(msg)
            raise HTTPException(409, msg)
        uow.commit()

    task_id = q_adapter.add_task("shorten_url", UrlShorten(url=body.url))
    return task_id


@router.delete(
    "/{url_id}",
    status_code=204,
    responses={404: {"description": "Url does not exist!"}},
)
def delete_url(
    url_id: int,
    uow: IUnitOfWork = Depends(unit_of_work),
) -> None:
    with uow:
        try:
            uow.urls.delete(url_id)
        except ResourceDoesNotExist:
            msg = f"Url with id: {url_id} does not exist!"
            logger.error(msg)
            raise HTTPException(404, msg)

        uow.commit()


@router.get("/redirect")
def redirect_to_url(
    short_url: str = Query(...),
    uow: IUnitOfWork = Depends(unit_of_work),
) -> RedirectResponse:
    with uow:
        try:
            full_url = uow.urls.get_by_short_url(short_url).url
        except ResourceDoesNotExist:
            msg = f"Short URL: {short_url} does not exist!"
            logger.error(msg)
            raise HTTPException(404, msg)

    return RedirectResponse(url=full_url)
