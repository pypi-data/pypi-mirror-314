from abc import ABC, abstractmethod
from datetime import date

from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders


class BaseSource(ABC):

    @abstractmethod
    def get_monthly_tenders(self, start_date: date, end_date: date) -> Tenders:
        pass  # pragma: no cover

    @abstractmethod
    def get_tender(self, code: str) -> Tender:
        pass  # pragma: no cover

    @abstractmethod
    def get_purchase_order(self, code: str) -> PurchaseOrder:
        pass  # pragma: no cover
