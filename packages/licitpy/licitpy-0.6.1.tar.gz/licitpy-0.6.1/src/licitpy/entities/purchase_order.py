from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import HttpUrl

from licitpy.services.purchase_order import PurchaseOrderServices
from licitpy.types.geography import Commune, Region
from licitpy.types.purchase_order import Status


class PurchaseOrder:

    def __init__(
        self,
        code: str,
        status: Optional[Status] = None,
        title: Optional[str] = None,
        issue_date: Optional[date] = None,
        region: Optional[Region] = None,
        commune: Optional[Commune] = None,
        services: Optional[PurchaseOrderServices] = None,
    ):

        self.code: str = code

        self._url: Optional[HttpUrl] = None
        self._html: Optional[str] = None

        self._status: Optional[Status] = status
        self._title: Optional[str] = title
        self._issue_date: Optional[date] = issue_date
        self._region: Optional[Region] = region
        self._commune: Optional[Commune] = commune

        self._tender_code: Optional[str] = None

        self.services = services or PurchaseOrderServices()

    @property
    def url(self) -> HttpUrl:
        if self._url is None:
            self._url = self.services.get_url(self.code)
        return self._url

    @property
    def html(self) -> str:
        if self._html is None:
            self._html = self.services.get_html(self.url)
        return self._html

    @property
    def status(self) -> Status:
        if self._status is None:
            self._status = self.services.get_status(self.html)
        return self._status

    @property
    def title(self) -> str:
        if self._title is None:
            self._title = self.services.get_title(self.html)
        return self._title

    @property
    def issue_date(self) -> date:
        if self._issue_date is None:
            self._issue_date = self.services.get_issue_date(self.html)
        return self._issue_date

    @property
    def tender_code(self) -> str | None:
        if self._tender_code is None:
            self._tender_code = self.services.get_tender_code(self.html)
        return self._tender_code

    @property
    def commune(self) -> Commune:
        if self._commune is None:
            self._commune = self.services.get_commune(self.html)
        return self._commune

    @property
    def region(self) -> Region:
        if self._region is None:
            self._region = self.services.get_region(self.commune)
        return self._region

    @classmethod
    def create(cls, code: str) -> PurchaseOrder:
        return cls(code)

    @classmethod
    def from_data(
        cls,
        code: str,
        *,
        status: Optional[Status] = None,
        title: Optional[str] = None,
        services: Optional[PurchaseOrderServices] = None,
    ) -> PurchaseOrder:
        return cls(code, status=status, title=title, services=services)
