from datetime import date
import unicodedata

from pydantic import HttpUrl

from licitpy.parsers.base import BaseParser
from licitpy.types.geography import Commune, GeographyChile, Region
from licitpy.types.purchase_order import Status
from licitpy.utils.date import convert_to_date


class PurchaseOrderParser(BaseParser):

    def get_url_from_code(self, code: str) -> HttpUrl:
        """Get the URL of a purchase order from the code."""
        url = f"https://www.mercadopublico.cl/PurchaseOrder/Modules/PO/DetailsPurchaseOrder.aspx?codigoOC={code}"
        return HttpUrl(url)

    def get_purchase_order_status(self, html: str) -> Status:
        """Get the status of a purchase order from the HTML content."""
        status = self.get_text_by_element_id(html, "lblStatusPOValue")

        # Generates the same process as performed in
        # PurchaseOrderDownloader:get_purchase_orders_from_csv -> df["Estado"]

        # Normalize the text to remove accents
        normalized_text = unicodedata.normalize("NFKD", status)

        status = "".join(
            char for char in normalized_text if not unicodedata.combining(char)
        )

        return Status(status)

    def get_purchase_order_title_from_html(self, html: str) -> str:
        """Get the title of a purchase order from the HTML content."""
        return self.get_text_by_element_id(html, "lblNamePOValue")

    def get_purchase_order_issue_date_from_html(self, html: str) -> date:
        """Get the issue date of a purchase order from the HTML content."""
        # 06-12-2024 - DD-MM-YYYY
        issue_date = self.get_text_by_element_id(html, "lblCreationDatePOValue")
        return convert_to_date(issue_date)

    def get_purchase_order_tender_code_from_html(self, html: str) -> str | None:
        """Get the tender code of a purchase order from the HTML content."""
        if not self.has_element_id(html, "lblProvenience"):
            return None

        return self.get_text_by_element_id(html, "lblProvenienceValue")

    def get_purchase_order_commune_from_html(self, html: str) -> Commune:
        """Get the commune of a purchase order from the HTML content."""
        return Commune(self.get_text_by_element_id(html, "lblCommuneValuePF"))

    def get_purchase_order_region_from_html(self, commune: Commune) -> Region:
        """Get the region of a purchase order from the commune."""
        return GeographyChile[commune].region
