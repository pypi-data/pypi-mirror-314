from datetime import date

from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.entities.purchase_orders import PurchaseOrders
from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders
from licitpy.sources.base import BaseSource


class API(BaseSource):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_monthly_tenders(self, start_date: date, end_date: date) -> Tenders:
        raise NotImplementedError("This method has not been implemented yet.")

    def get_tender(self, code: str) -> Tender:
        raise NotImplementedError("This method has not been implemented yet.")

    def get_purchase_order(self, code: str) -> PurchaseOrder:
        raise NotImplementedError("This method has not been implemented yet.")

    def get_monthly_purchase_orders(
        self, start_date: date, end_date: date
    ) -> PurchaseOrders:
        raise NotImplementedError("This method has not been implemented yet.")
