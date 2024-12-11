from __future__ import annotations

from operator import attrgetter
from typing import Iterator, List

import pandas

from licitpy.entities.tender import Tender
from licitpy.types.geography import Region
from licitpy.types.tender.status import Status
from licitpy.types.tender.tender import Tier


class Tenders:
    def __init__(self, tenders: List[Tender]):
        self._tenders = sorted(tenders, key=attrgetter("code"), reverse=True)

    def by_budget_tier(self, tier: Tier) -> Tenders:
        return Tenders([tender for tender in self._tenders if tender.tier == tier])

    def with_status(self, status: Status) -> Tenders:
        tenders = [tender for tender in self._tenders if tender.status == status]
        return Tenders(tenders)

    def in_region(self, region: Region) -> Tenders:

        tenders = [tender for tender in self._tenders if tender.region == region]
        return Tenders(tenders)

    def to_pandas(self) -> pandas.DataFrame:
        raise NotImplementedError

    @classmethod
    def from_tenders(cls, tenders: List[Tender]) -> Tenders:
        return cls(tenders)

    @property
    def codes(self) -> List[str]:
        return [tender.code for tender in self._tenders]

    def limit(self, limit: int) -> Tenders:
        return Tenders(self._tenders[:limit])

    def count(self) -> int:
        return len(self._tenders)

    def __iter__(self) -> Iterator[Tender]:
        return iter(self._tenders)

    def __getitem__(self, index: int) -> Tender:
        return self._tenders[index]
