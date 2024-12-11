import re
from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

from lxml.html import HtmlElement
from pydantic import HttpUrl

from licitpy.parsers.base import BaseParser
from licitpy.types.attachments import Attachment, FileType
from licitpy.types.geography import Region
from licitpy.types.tender.open_contract import OpenContract, PartyRoleEnum
from licitpy.types.tender.status import StatusFromImage, StatusFromOpenContract
from licitpy.types.tender.tender import Tier


class TenderParser(BaseParser):

    def get_tender_opening_date_from_tender_ocds_data(
        self, data: OpenContract
    ) -> datetime:

        # The date comes as if it were UTC, but it is actually America/Santiago
        # - 2024-11-06T11:40:34Z -> 2024-11-06 11:40:34-03:00

        tender = data.records[0].compiledRelease.tender
        start_date = tender.tenderPeriod.startDate

        return datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=ZoneInfo("America/Santiago")
        )

    def get_closing_date_from_tender_ocds_data(self, data: OpenContract) -> datetime:
        tender = data.records[0].compiledRelease.tender
        end_date = tender.tenderPeriod.endDate

        return datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=ZoneInfo("America/Santiago")
        )

    def get_tender_status_from_tender_ocds_data(
        self, data: OpenContract
    ) -> StatusFromOpenContract:
        tender = data.records[0].compiledRelease.tender
        return tender.status

    def get_tender_title_from_tender_ocds_data(self, data: OpenContract) -> str:
        tender = data.records[0].compiledRelease.tender
        return tender.title

    def get_tender_description_from_tender_ocds_data(self, data: OpenContract) -> str:
        tender = data.records[0].compiledRelease.tender
        return tender.description

    def get_tender_region_from_tender_ocds_data(self, data: OpenContract) -> Region:

        parties = data.records[0].compiledRelease.parties

        procuring_entities = [
            party for party in parties if PartyRoleEnum.PROCURING_ENTITY in party.roles
        ]

        if len(procuring_entities) != 1:
            raise ValueError(
                "There must be exactly one entity with the role of procuringEntity."
            )

        address = procuring_entities[0].address

        if address is None or address.region is None:
            raise ValueError(
                "The address or region is missing for the procuring entity."
            )

        return address.region

    def get_tender_tier(self, code: str) -> Tier:
        return Tier(code.split("-")[-1:][0][:2])

    def get_tender_status_from_image(self, html: str) -> StatusFromImage:
        status = self.get_src_by_element_id(html, "imgEstado")
        return StatusFromImage(status.split("/")[-1].replace(".png", "").upper())

    def get_tender_code_from_tender_ocds_data(self, data: OpenContract) -> str:
        return str(data.uri).split("/")[-1].strip()

    def _get_table_attachments(self, html: str) -> HtmlElement:
        table = self.get_html_element_by_id(html, "DWNL_grdId")
        if not table:
            raise ValueError("Table with ID 'DWNL_grdId' not found")
        return table[0]

    def _get_table_attachments_rows(self, table: HtmlElement) -> List[HtmlElement]:
        rows = table.xpath("tr[@class]")
        if not rows:
            raise ValueError("No rows found in the table")
        return rows

    def _parse_size_attachment(self, td: HtmlElement) -> int:
        size_text: str = td.xpath("span/text()")[0]

        try:
            return int(size_text.replace(" Kb", "").strip()) * 1024
        except ValueError:
            raise ValueError(f"Invalid size format: {size_text}")

    def _extract_attachment_id(self, td: HtmlElement) -> str:

        input_id = td.xpath("input/@id")
        if not input_id:
            raise ValueError("No input ID found in the first column")

        match = re.search(r"ctl(\d+)", input_id[0])
        if not match:
            raise ValueError("No match found for attachment ID")

        return match.group(1)

    def _extract_content_from_attachment_row(self, td: HtmlElement) -> str | None:
        content = td.xpath("span/text()")

        if content:
            return content[0]

        return None

    def get_attachments(self, html: str) -> List[Attachment]:

        table = self._get_table_attachments(html)
        rows: List[HtmlElement] = self._get_table_attachments_rows(table)

        attachments: List[Attachment] = []

        for tr in rows:
            td: List[HtmlElement] = tr.xpath("td")

            attachment_id: str = self._extract_attachment_id(td[0])
            name = self._extract_content_from_attachment_row(td[1])
            attachment_type = self._extract_content_from_attachment_row(td[2])
            description = self._extract_content_from_attachment_row(td[3])
            size: int = self._parse_size_attachment(td[4])
            upload_date = self._extract_content_from_attachment_row(td[5])

            if not name:
                raise ValueError("Attachment name not found")

            # Bases_686617-1-L124.pdf
            file_type = FileType(name.split(".")[-1])

            attachment = Attachment(
                **{
                    "id": attachment_id,
                    "name": name,
                    "type": attachment_type,
                    "description": description,
                    "size": size,
                    "upload_date": upload_date,
                    "file_type": file_type,
                }
            )

            attachments.append(attachment)

        return attachments

    def get_attachment_url_from_html(self, html: str) -> HttpUrl:

        attachment_url = self.get_on_click_by_element_id(html, "imgAdjuntos")

        url_match = re.search(r"ViewAttachment\.aspx\?enc=(.*)','", attachment_url)

        if not url_match:
            raise ValueError("Attachment URL hash not found")

        enc: str = url_match.group(1)
        url = f"https://www.mercadopublico.cl/Procurement/Modules/Attachment/ViewAttachment.aspx?enc={enc}"

        return HttpUrl(url)

    def get_tender_purchase_order_url(self, html: str) -> HttpUrl:

        purchase_order_popup = self.get_href_by_element_id(html, "imgOrdenCompra")

        if not purchase_order_popup:
            raise ValueError("Purchase orders not found")

        match = re.search(r"qs=(.*)$", purchase_order_popup)

        if not match:
            raise ValueError("Purchase Order query string not found")

        qs = match.group(1)
        url = f"https://www.mercadopublico.cl/Procurement/Modules/RFB/PopUpListOC.aspx?qs={qs}"

        return HttpUrl(url)

    def get_purchase_orders_codes_from_html(self, html: str) -> List[str]:
        codes = re.findall(r'id="(rptSearchOCDetail_ctl\d{2}_lkNumOC)"', html)
        return [self.get_text_by_element_id(html, xpath) for xpath in codes]

    def get_questions_url(self, html: str) -> HttpUrl:

        href = self.get_href_by_element_id(html, "imgPreguntasLicitacion")
        match = re.search(r"qs=(.*)$", href)

        if not match:
            raise ValueError("Questions query string not found")

        qs = match.group(1)
        url = f"https://www.mercadopublico.cl/Foros/Modules/FNormal/PopUps/PublicView.aspx?qs={qs}"

        return HttpUrl(url)

    def get_question_code(self, html: str) -> str:
        return self.get_value_by_element_id(html, "h_intRBFCode")
