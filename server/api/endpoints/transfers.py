from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from loguru import logger

from adapters.repository import (
    AbstractRepository,
    ResourceDoesNotExist,
)
from models import transfer as model


router = APIRouter()
#
#
# @router.get("/{transfer_id}")
# def get(
#     transfer_id: int,
#     repo: AbstractRepository = Depends(get_repository)
# ) -> model.Transfer:
#     try:
#         return repo.get_transfer(transfer_id)
#     except ResourceDoesNotExist as ex:
#         logger.exception(str(ex))
#         raise HTTPException(404, str(ex))
#
#
# @router.get("/")
# def get_all(repo: AbstractRepository = Depends(get_repository)):
#     return repo.get_transfers()
#
#
# @router.post("/")
# def create_transfer(
#     transfer: model.TransferIn,
#     repo: AbstractRepository = Depends(get_repository),
# ) -> model.Transfer:
#     try:
#         return repo.create_transfer(transfer.dict())
#     except ResourceDoesNotExist as ex:
#         logger.exception(str(ex), 404)
#         raise HTTPException(404, str(ex))
#
#
# @router.patch("/{transfer_id}")
# def update_transfer(
#     transfer_id: int,
#     transfer_upd: model.TransferUpd,
#     repo: AbstractRepository = Depends(get_repository),
# ) -> model.Transfer:
#     try:
#         return repo.update_transfer(transfer_id, transfer_upd.dict(exclude_unset=True))
#     except ResourceDoesNotExist as ex:
#         logger.exception(str(ex), 404)
#         raise HTTPException(404, str(ex))
#
#
# @router.delete(
#     "/{transfer_id}",
#     status_code=204,
# )
# def delete_transfer(
#     transfer_id: int,
#     repo: AbstractRepository = Depends(get_repository),
# ):
#     try:
#         return repo.delete_transfer(transfer_id)
#     except ResourceDoesNotExist as ex:
#         logger.exception(str(ex), 404)
#         raise HTTPException(404, str(ex))