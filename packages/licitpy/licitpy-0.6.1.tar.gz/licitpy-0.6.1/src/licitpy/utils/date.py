from datetime import date, datetime, timedelta
from typing import Tuple, Union
from zoneinfo import ZoneInfo

from licitpy.types.search import TimeRange


def convert_to_date(date_value: str | date) -> date:
    """
    Convert a given input into a date object.

    This function handles the following scenarios:
    - If `date_value` is already a `date` instance, it is returned directly.
    - If `date_value` is a string, this function attempts to parse it.
      First, it tries ISO format (YYYY-MM-DD). If that fails, it tries the format (dd-mm-YYYY).
      If both fail, a ValueError is raised.

    Returns:
        date: A Python date object.

    Raises:
        ValueError: If the string does not match the expected formats.
        TypeError: If the input is neither a string nor a date.
    """

    # If it's already a date, just return it
    if isinstance(date_value, date):
        return date_value

    # If it's a string, attempt to parse it
    if isinstance(date_value, str):
        # Try ISO format first
        try:
            # eg : "yyyy-mm-dd"
            return date.fromisoformat(date_value)
        except ValueError:
            pass  # Try the next format

        # Try dd-mm-yyyy
        try:
            return datetime.strptime(date_value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError(
                f"The date string '{date_value}' does not match ISO (YYYY-MM-DD) "
                "or dd-mm-yyyy formats."
            )

    # If the input is neither a string nor a date object
    raise TypeError(f"Expected str or date, got {type(date_value)}")


def convert_to_datetime(
    date_str: str, input_format: str, timezone: str = "America/Santiago"
) -> datetime:
    """
    Converts a date string from a specified format to a datetime object
    with the given timezone.

    Args:
        date_str (str): The date string to convert.
        input_format (str): The format of the input date string (e.g., '%d-%m-%Y %H:%M:%S').
        timezone (str): The timezone to apply. Default is 'America/Santiago'.

    Returns:
        datetime: The converted datetime object with the specified timezone.

    Raises:
        ValueError: If the date string does not match the input format.
    """
    try:
        # Parse the date string using the provided format
        parsed_date = datetime.strptime(date_str, input_format)
        # Apply the specified timezone
        return parsed_date.replace(tzinfo=ZoneInfo(timezone))
    except ValueError:
        raise ValueError(
            f"Invalid date format: {date_str}. Expected format: '{input_format}'"
        )


def _time_range(time_range: TimeRange) -> Tuple[date, date]:
    today = date.today()
    yesterday = today - timedelta(days=1)
    beginning_of_month = today.replace(day=1)

    if time_range == TimeRange.TODAY:
        return today, today
    elif time_range == TimeRange.FROM_YESTERDAY:
        return yesterday, yesterday
    elif time_range == TimeRange.THIS_MONTH:
        return beginning_of_month, today
    else:
        raise ValueError(f"Unsupported time range: {time_range}")


def determine_date_range(
    start_date: Union[str, date, None] = None,
    end_date: Union[str, date, None] = None,
    time_range: TimeRange = TimeRange.THIS_MONTH,
) -> Tuple[date, date]:

    if start_date is not None and end_date is not None:

        start_date = convert_to_date(start_date)
        end_date = convert_to_date(end_date)

        if end_date < start_date:
            raise ValueError("Start date cannot be greater than end date")

        return start_date, end_date

    return _time_range(time_range)
