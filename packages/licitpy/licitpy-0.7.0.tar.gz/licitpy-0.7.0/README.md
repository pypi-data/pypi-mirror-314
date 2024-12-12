# Licitpy

LicitPy: A Python toolbox designed for downloading, parsing, and analyzing public tenders from Chile's Mercado Público.

## Install

```bash
pip install licitpy
```

## Example

### Tenders

- Get tenders from today, with budget tier L1, in region IV, and limit to 10 tenders

```python
from pprint import pprint

from licitpy import Licitpy
from licitpy.types import Region, Tier, TimeRange

licitpy = Licitpy()

tenders = (
    licitpy.tenders.from_date(time_range=TimeRange.TODAY)
    .by_budget_tier(Tier.L1)
    .in_region(Region.IV)
    .limit(10)
)

for tender in tenders:
    pprint(
        {
            "url": tender.url,
            "code": tender.code,
            "title": tender.title,
            "status": tender.status,
            "opening_date": tender.opening_date,
            "region": tender.region,
        }
    )
```
