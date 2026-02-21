from datetime import datetime

from app.core.config import settings


def parse_timestamp(value: str) -> datetime:
    return datetime.strptime(value, settings.datetime_format)


def to_timestamp(dt: datetime) -> str:
    return dt.strftime(settings.datetime_format)


def in_inclusive_range(ts: datetime, start: datetime, end: datetime) -> bool:
    return start <= ts <= end
