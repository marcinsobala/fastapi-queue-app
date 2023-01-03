from abc import ABC, abstractmethod
from typing import Any, Callable

from sqlalchemy.orm import Session

from adapters.database import (
    CurrencyDb,
    TransferDb,
    UserDb,
)


class AcronymAlreadyExists(Exception):
    pass


class ResourceDoesNotExist(Exception):
    pass


class CurrencyIsUsedInTransfer(Exception):
    pass


class AbstractRepository(ABC):
    @abstractmethod
    def get_currency(self, currency_id: int):
        pass

    @abstractmethod
    def get_currencies(self, filters: dict[str, Any] | None = None):
        pass

    @abstractmethod
    def create_currency(self, create_data: dict[str, Any]):
        pass

    @abstractmethod
    def update_currency(self, currency_id: int, update_data: dict[str, Any]):
        pass

    @abstractmethod
    def delete_currency(self, currency_id: int):
        pass

    @abstractmethod
    def get_transfer(self, transfer_id: int):
        pass

    @abstractmethod
    def get_transfers(self, filters: dict[str, Any] | None = None):
        pass

    @abstractmethod
    def create_transfer(self, create_data: dict[str, Any]):
        pass

    @abstractmethod
    def update_transfer(self, transfer_id: int, update_data: dict[str, Any]):
        pass

    @abstractmethod
    def delete_transfer(self, transfer_id: int):
        pass


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session_maker: Callable[[], Session]):
        self.session: Session = session_maker()
        
    def close_session(self):
        self.session.close()

    def get_currency(self, currency_id: int):
        currency = self.session.get(CurrencyDb, currency_id)
        if currency is None:
            raise ResourceDoesNotExist(f"Currency with id {currency_id} not found")
        return currency

    def get_currencies(self, filters: dict[str, Any] | None = None):
        return self.session.query(CurrencyDb).filter_by(**filters or {}).all()

    def create_currency(self, create_data: dict[str, Any]):
        new_currency = CurrencyDb(**create_data)
        with self.session.begin():
            self.session.add(new_currency)

        return self.session.get(CurrencyDb, new_currency.id)

    def update_currency(self, currency_id: int, update_data: dict[str, Any]):
        with self.session.begin():
            currency = self.get_currency(currency_id)
            for key, value in update_data.items():
                setattr(currency, key, value)
                
        self.session.refresh(currency)
        return currency

    def delete_currency(self, currency_id: int):
        with self.session.begin():
            transfers = self.get_transfers({"currency_id": currency_id})
            if transfers:
                raise CurrencyIsUsedInTransfer(
                    f"{len(transfers)} transfers were already made with currency: {currency_id}"
                )
            
            rows_deleted = self.session.query(
                CurrencyDb
            ).where(
                CurrencyDb.id == currency_id
            ).delete()
        if rows_deleted is 0:
            raise ResourceDoesNotExist(f"Currency with id {currency_id} not found")

    def get_transfer(self, transfer_id: int):
        transfer = self.session.get(TransferDb, transfer_id)
        if transfer is None:
            raise ResourceDoesNotExist(f"Transfer with id {transfer_id} not found")
        return transfer

    def get_transfers(self, filters: dict[str, Any] | None = None):
        return self.session.query(TransferDb).filter_by(**filters or {}).all()

    def create_transfer(self, create_data: dict[str, Any]):
        new_transfer = TransferDb(**create_data)
        with self.session.begin():
            self.get_user(new_transfer.user_id)
            self.get_currency(new_transfer.currency_id)
            self.session.add(new_transfer)

        return self.session.get(TransferDb, new_transfer.id)

    def update_transfer(self, transfer_id: int, update_data: dict[str, Any]):
        with self.session.begin():
            if "currency_id" in update_data:
                self.get_currency(update_data["currency_id"])
            if "user_id" in update_data:
                self.get_currency(update_data["currency_id"])
            transfer = self.get_transfer(transfer_id)
            for key, value in update_data.items():
                setattr(transfer, key, value)

        self.session.refresh(transfer)
        return transfer

    def delete_transfer(self, transfer_id: int):
        with self.session.begin():
            rows_deleted = self.session.query(
                TransferDb
            ).where(
                TransferDb.id == transfer_id
            ).delete()
        if rows_deleted is 0:
            raise ResourceDoesNotExist(f"Transfer with id {transfer_id} not found")
