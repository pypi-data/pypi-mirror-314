from datetime import datetime, timedelta


def time_mills_from_now(interval_days: int = 0):
    """
    Returns the current time in milliseconds plus the interval in days.
    @param interval_days: The number of days to add to the current time.
    """

    now = datetime.now()
    future_time = now + timedelta(days=interval_days)
    return int(future_time.timestamp() * 1000)


def last_moment_of_day(interval_days: int = 0):
    """
    Returns the last moment of the day in milliseconds plus the interval in days.
    @param interval_days: The number of days to add to the current day.
    """

    now = datetime.now()
    future_time = now + timedelta(days=interval_days)
    future_time = future_time.replace(hour=23, minute=59, second=59, microsecond=999)
    return int(future_time.timestamp() * 1000)


def format_timestamp(timestamp: int) -> str:
    """Format timestamp to a readable date string."""
    return datetime.fromtimestamp(
        timestamp / 1000, tz=datetime.now().astimezone().tzinfo
    ).strftime("%Y-%m-%d %H:%M:%S")
