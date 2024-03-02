from adapters.queue import celery_app
from core.unit_of_work import SqlAlchemyUnitOfWork
from core.url_shortener import generate_short_url


@celery_app.task(name="shorten_url")
def add_short_url(url: str) -> str:
    short_url = generate_short_url()
    uow = SqlAlchemyUnitOfWork()
    with uow:
        uow.urls.update_with_short_url(url=url, short_url=short_url)
        uow.commit()
    return short_url
