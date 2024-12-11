from datetime import timedelta
from typing import Union

from licitpy.client.purchase_orders import PurchaseOrdersClient
from licitpy.client.tenders import TendersClient
from licitpy.services.purchase_order import PurchaseOrderServices
from licitpy.services.tender import TenderServices
from licitpy.settings import settings
from licitpy.sources import API, Local


class Licitpy:
    
    def __init__(
        self,
        api_key: str | None = None,
        use_cache: bool = settings.use_cache,
        expire_after: timedelta = settings.cache_expire_after,
        disable_progress_bar: bool = settings.disable_progress_bar,
    ):

        settings.use_cache = use_cache
        settings.cache_expire_after = expire_after
        settings.disable_progress_bar = disable_progress_bar

        purchase_order_services = PurchaseOrderServices()
        tender_services = TenderServices()

        self.source: Union[API, Local] = (
            API(api_key=api_key)
            if api_key
            else Local(
                purchase_order_services=purchase_order_services,
                tender_services=tender_services,
            )
        )

    @property
    def tenders(self) -> TendersClient:
        return TendersClient(self.source)

    @property
    def purchase_orders(self) -> PurchaseOrdersClient:
        return PurchaseOrdersClient(self.source)
