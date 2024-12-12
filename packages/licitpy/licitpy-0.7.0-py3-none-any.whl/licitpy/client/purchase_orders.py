from datetime import date
from typing import Union

from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.entities.purchase_orders import PurchaseOrders
from licitpy.sources import API, Local
from licitpy.types.search import TimeRange
from licitpy.utils.date import determine_date_range


class PurchaseOrdersClient:
    def __init__(self, source: Union[API, Local]) -> None:
        self.source = source

    def from_date(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        time_range: TimeRange = TimeRange.THIS_MONTH,
    ) -> PurchaseOrders:

        start_date, end_date = determine_date_range(start_date, end_date, time_range)

        return self.source.get_monthly_purchase_orders(start_date, end_date)

    def from_code(self, code: str) -> PurchaseOrder:
        return self.source.get_purchase_order(code)
