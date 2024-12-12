from enum import Enum


class TimeRange(Enum):
    TODAY = "today"
    FROM_YESTERDAY = "from_yesterday"
    THIS_MONTH = "this_month"
