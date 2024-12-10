from datetime import datetime, timedelta
from typing import TypedDict

import pytz


class DateRange(TypedDict):
    date: str
    timestamp: int


class DayRange(TypedDict):
    start: DateRange
    end: DateRange


def get_day_range(days_ago: int = 0, timezone: str = "Asia/Shanghai") -> DayRange:
    """Get the start and end timestamps for a specific day.

    Args:
        days_ago: Number of days to look back (default: 0 for today)
        timezone: Timezone string (default: 'Asia/Shanghai')

    Returns:
        DayRange containing start and end timestamps and formatted dates

    Examples:
        >>> result = get_day_range(1)  # Get yesterday's range
        >>> print(result['start']['date'])  # '2024-01-01 00:00:00'
        >>> print(result['end']['date'])    # '2024-01-01 23:59:59'
    """
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)

    # Get start of the target day
    target_day = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(
        days=days_ago
    )

    # Calculate timestamps
    start_timestamp = int(target_day.timestamp())
    end_timestamp = start_timestamp + 24 * 60 * 60 - 1

    # Format dates
    start_date = datetime.fromtimestamp(start_timestamp, tz).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    end_date = datetime.fromtimestamp(end_timestamp, tz).strftime("%Y-%m-%d %H:%M:%S")

    return {
        "start": {"date": start_date, "timestamp": start_timestamp},
        "end": {"date": end_date, "timestamp": end_timestamp},
    }
