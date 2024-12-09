from datetime import date
from typing import Union

from licitpy.entities.tender import Tender
from licitpy.entities.tenders import Tenders
from licitpy.sources import API, Local
from licitpy.types.search import TimeRange
from licitpy.utils.date import determine_date_range


class TendersClient:
    def __init__(self, source: Union[API, Local]) -> None:
        self.source = source

    def from_date(
        self,
        start_date: str | date | None = None,
        end_date: str | date | None = None,
        time_range: TimeRange = TimeRange.THIS_MONTH,
    ) -> Tenders:

        start_date, end_date = determine_date_range(start_date, end_date, time_range)

        return self.source.get_monthly_tenders(start_date, end_date)

    def from_code(self, code: str) -> Tender:
        return self.source.get_tender(code)
