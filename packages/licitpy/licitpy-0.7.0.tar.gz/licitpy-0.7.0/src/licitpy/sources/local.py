from datetime import date
from typing import List, Optional, Tuple

from dateutil.relativedelta import relativedelta

from licitpy.entities.purchase_order import PurchaseOrder
from licitpy.entities.purchase_orders import PurchaseOrders
from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders
from licitpy.services.purchase_order import PurchaseOrderServices
from licitpy.services.tender import TenderServices
from licitpy.sources.base import BaseSource
from licitpy.types.purchase_order import PurchaseOrderFromCSV
from licitpy.types.tender.status import Status as TenderStatus
from licitpy.types.tender.tender import TenderFromCSV


class Local(BaseSource):
    def __init__(
        self,
        tender_services: Optional[TenderServices] = None,
        purchase_order_services: Optional[PurchaseOrderServices] = None,
    ) -> None:

        self.tender_services = tender_services or TenderServices()
        self.purchase_order_services = (
            purchase_order_services or PurchaseOrderServices()
        )

    def get_monthly_tenders(self, start_date: date, end_date: date) -> Tenders:

        year_month: List[Tuple[int, int]] = []

        current_date = start_date
        while current_date <= end_date:

            year_month.append((current_date.year, current_date.month))
            current_date += relativedelta(months=1)

        tenders: List[TenderFromCSV] = []

        for year, month in year_month:
            tenders += self.tender_services.get_tenders(year, month)

        # Explanation regarding the tender status:
        # Tenders can have their status sourced from three different data origins:
        # 1. The Mercado Publico API
        # 2. A CSV file from Mercado Publico
        # 3. The HTML content of the tender page
        #
        # Each data source uses a different format to represent the tender status:
        # - In the CSV, a published tender is labeled as "Publicada".
        # - In the HTML, a published tender is labeled as "Publicadas" (with an additional "s").
        # - In the API, a published tender is represented as "active".
        #
        # To address these differences, we created two Enum classes to map and standardize the tender status:
        # 1. `StatusFromCSV`: Represents the status as it appears in the CSV file (e.g., "Publicada").
        # 2. `Status` (or `TenderStatus`): Represents the unified status format used internally across the application (e.g., "PUBLISHED").
        #
        # The transition from `StatusFromCSV` to `Status` ensures consistency:
        # - `StatusFromCSV` captures the raw status from the CSV, using the same value as in the source.
        # - `Status` standardizes these values into a common format, such as "PUBLISHED", that is used internally.
        #
        # The mapping works as follows:
        # - `tender.Estado.name` retrieves the raw status (e.g., "Publicada") from the CSV.
        # - This raw status is converted to the corresponding standardized value in `Status` (e.g., "PUBLISHED").
        #
        # Example:
        # - `StatusFromCSV.PUBLISHED` maps the CSV value "Publicada".
        # - `Status.PUBLISHED` is the standardized internal representation used in the application.
        #
        # This approach ensures that regardless of the data source, all tender statuses are consistent and uniform.

        return Tenders.from_tenders(
            [
                Tender(
                    tender.CodigoExterno,
                    region=tender.RegionUnidad,
                    status=TenderStatus(tender.Estado.name),
                    title=tender.Nombre,
                    description=tender.Descripcion,
                    opening_date=tender.FechaPublicacion,
                    services=self.tender_services,
                )
                for tender in tenders
                if start_date <= tender.FechaPublicacion <= end_date
            ]
        )

    def get_tender(self, code: str) -> Tender:
        return Tender(code)

    def get_monthly_purchase_orders(
        self, start_date: date, end_date: date
    ) -> PurchaseOrders:

        year_month: List[Tuple[int, int]] = []

        current_date = start_date
        while current_date <= end_date:

            year_month.append((current_date.year, current_date.month))
            current_date += relativedelta(months=1)

        purchase_orders: List[PurchaseOrderFromCSV] = []

        for year, month in year_month:

            purchase_orders += self.purchase_order_services.get_purchase_orders(
                year, month
            )

        return PurchaseOrders.from_purchase_orders(
            [
                PurchaseOrder(
                    purchase_order.Codigo,
                    status=purchase_order.Estado,
                    title=purchase_order.Nombre,
                    issue_date=purchase_order.FechaEnvio,
                    region=purchase_order.RegionUnidadCompra,
                    commune=purchase_order.CiudadUnidadCompra,
                    services=self.purchase_order_services,
                )
                for purchase_order in purchase_orders
                if start_date <= purchase_order.FechaEnvio <= end_date
            ]
        )

    def get_purchase_order(self, code: str) -> PurchaseOrder:
        return PurchaseOrder.create(code)
