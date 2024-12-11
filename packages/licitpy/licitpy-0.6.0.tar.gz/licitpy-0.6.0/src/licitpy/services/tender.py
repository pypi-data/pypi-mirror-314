from datetime import datetime
from functools import partial
from typing import List, Optional
from zoneinfo import ZoneInfo

from pydantic import HttpUrl

from licitpy.downloader.tender import TenderDownloader
from licitpy.entities.purchase_orders import PurchaseOrders
from licitpy.parsers.tender import TenderParser
from licitpy.types.attachments import Attachment
from licitpy.types.tender.open_contract import OpenContract
from licitpy.types.tender.status import Status, StatusFromOpenContract
from licitpy.types.tender.tender import Question, Region, TenderFromCSV, Tier


class TenderServices:

    def __init__(
        self,
        downloader: Optional[TenderDownloader] = None,
        parser: Optional[TenderParser] = None,
    ):

        self.downloader: TenderDownloader = downloader or TenderDownloader()
        self.parser: TenderParser = parser or TenderParser()

    def get_status(self, data: OpenContract) -> Status:

        closing_date = self.parser.get_closing_date_from_tender_ocds_data(data)
        status = self.parser.get_tender_status_from_tender_ocds_data(data)

        # If the tender is published (active) but the closing date has passed,
        # the status must be verified using the status image.

        if status == StatusFromOpenContract.PUBLISHED and not self.is_open(
            closing_date
        ):

            html = self.get_html_from_ocds_data(data)
            status_from_image = self.parser.get_tender_status_from_image(html)

            return Status(status_from_image.name)

        return Status(status.name)

    def get_ocds_data(self, code: str) -> OpenContract:
        return self.downloader.get_tender_ocds_data_from_api(code)

    def get_url(self, code: str) -> HttpUrl:
        return self.downloader.get_tender_url_from_code(code)

    def get_title(self, data: OpenContract) -> str:
        return self.parser.get_tender_title_from_tender_ocds_data(data)

    def get_opening_date(self, data: OpenContract) -> datetime:
        return self.parser.get_tender_opening_date_from_tender_ocds_data(data)

    def get_html(self, url: HttpUrl) -> str:
        return self.downloader.get_html_from_url(url)

    def get_tenders(self, year: int, month: int) -> List[TenderFromCSV]:
        return self.downloader.get_tenders(year, month)

    def get_tier(self, code: str) -> Tier:
        return self.parser.get_tender_tier(code)

    def get_description(self, data: OpenContract) -> str:
        return self.parser.get_tender_description_from_tender_ocds_data(data)

    def get_region(self, data: OpenContract) -> Region:
        return self.parser.get_tender_region_from_tender_ocds_data(data)

    def get_closing_date(self, data: OpenContract) -> datetime:
        return self.parser.get_closing_date_from_tender_ocds_data(data)

    def get_code_from_ocds_data(self, data: OpenContract) -> str:
        return self.parser.get_tender_code_from_tender_ocds_data(data)

    def is_open(self, closing_date: datetime) -> bool:
        if not closing_date:
            return False

        now_utc = datetime.now(tz=ZoneInfo("America/Santiago"))
        return now_utc < closing_date

    def get_html_from_code(self, code: str) -> str:
        url = self.get_url(code)
        return self.get_html(url)

    def get_html_from_ocds_data(self, data: OpenContract) -> str:
        code = self.parser.get_tender_code_from_tender_ocds_data(data)
        return self.get_html_from_code(code)

    def get_attachment_url(self, html: str) -> HttpUrl:
        return self.parser.get_attachment_url_from_html(html)

    def get_attachments_from_url(self, url: HttpUrl) -> List[Attachment]:

        html = self.downloader.get_html_from_url(url)
        attachments: List[Attachment] = self.parser.get_attachments(html)

        for attachment in attachments:

            download_attachment_fn = partial(
                self.downloader.download_attachment, url, attachment
            )

            attachment._download_fn = download_attachment_fn

        return attachments

    def get_signed_base_from_attachments(
        self, attachments: List[Attachment]
    ) -> Attachment:

        signed_bases = [
            attachment
            for attachment in attachments
            if "Anexo Resolucion Electronica (Firmada)" in attachment.type
        ]

        if not signed_bases:
            raise ValueError("No signed base found in attachments.")

        return signed_bases[0]

    def get_tender_purchase_order_url(self, html: str) -> HttpUrl:
        return self.parser.get_tender_purchase_order_url(html)

    def get_tender_purchase_orders(self, html: str) -> PurchaseOrders:
        url = self.get_tender_purchase_order_url(html)

        html = self.downloader.get_html_from_url(url)
        codes = self.parser.get_purchase_orders_codes_from_html(html)

        return PurchaseOrders.from_tender(codes)

    def get_questions_url(self, html: str) -> HttpUrl:
        return self.parser.get_questions_url(html)

    def get_questions(self, url: HttpUrl) -> List[Question]:
        html = self.downloader.get_html_from_url(url)
        code = self.parser.get_question_code(html)

        return self.downloader.get_tender_questions(code)
