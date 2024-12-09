from datetime import datetime, timezone


def get_ntc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def parse_time_stamp(t) -> datetime:
    return datetime.fromtimestamp(t)


def to_time_utc_iso(dt: datetime) -> str:
    return dt.isoformat()


def to_time_utc_no_time_zone(dt: datetime) -> str:
    iso_str = dt.strftime("%Y-%m-%dT%H:%M:%S")
    return iso_str


def to_date_utc_no_time_zone(dt: datetime) -> str:
    iso_str = dt.strftime("%Y-%m-%dT00:00:00")
    return iso_str


def get_utc_now_edi_format() -> str:
    dt = get_ntc_now()
    return dt.strftime("%Y%m%d%H%M")
