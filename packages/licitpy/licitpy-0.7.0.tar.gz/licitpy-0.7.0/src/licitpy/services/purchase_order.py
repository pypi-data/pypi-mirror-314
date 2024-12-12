from datetime import date
from typing import List, Optional

from pydantic import HttpUrl

from licitpy.downloader.purchase_order import PurchaseOrderDownloader
from licitpy.parsers.purchase_order import PurchaseOrderParser
from licitpy.types.geography import Commune, Region
from licitpy.types.purchase_order import PurchaseOrderFromCSV, Status


class PurchaseOrderServices:

    def __init__(
        self,
        downloader: Optional[PurchaseOrderDownloader] = None,
        parser: Optional[PurchaseOrderParser] = None,
    ):

        self.downloader = downloader or PurchaseOrderDownloader()
        self.parser = parser or PurchaseOrderParser()

    def get_url(self, code: str) -> HttpUrl:
        return self.parser.get_url_from_code(code)

    def get_html(self, url: HttpUrl) -> str:
        return self.downloader.get_html_from_url(url)

    def get_status(self, html: str) -> Status:
        return self.parser.get_purchase_order_status(html)

    def get_title(self, html: str) -> str:
        return self.parser.get_purchase_order_title_from_html(html)

    def get_purchase_orders(self, year: int, month: int) -> List[PurchaseOrderFromCSV]:
        return self.downloader.get_purchase_orders(year, month)

    def get_issue_date(self, html: str) -> date:
        return self.parser.get_purchase_order_issue_date_from_html(html)

    def get_tender_code(self, html: str) -> str | None:
        return self.parser.get_purchase_order_tender_code_from_html(html)

    def get_commune(self, html: str) -> Commune:
        return self.parser.get_purchase_order_commune_from_html(html)

    def get_region(self, commune: Commune) -> Region:
        return self.parser.get_purchase_order_region_from_html(commune)
