from datetime import datetime
from datetime import timezone

import pytz
from bson import ObjectId
from pytz import timezone

LOCAL_TIME_ZONE = 'America/Sao_Paulo'
DATE_FORMAT_UTC = "%Y-%m-%dT%H:%M:%S.Z"
_month_labels = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


def get_month_by_index(index: int) -> str:
    return _month_labels[index - 1]


def get_month_by_index_str(index: str) -> str:
    return get_month_by_index(int(index))


def get_today_date_utc() -> str:
    return datetime.utcnow().replace(tzinfo=pytz.utc).strftime(DATE_FORMAT_UTC)


def timestamp_to_date_string(timestamp: float, time_zone: str = LOCAL_TIME_ZONE) -> str:
    timestamp = timestamp / 1000
    return str(datetime.fromtimestamp(timestamp, tz=timezone(time_zone)))


def get_current_year() -> int:
    return datetime.now().year


def object_id_to_date(object_id: ObjectId) -> str:
    timestamp = object_id.generation_time
    return datetime.utcfromtimestamp(timestamp.timestamp()).strftime(DATE_FORMAT_UTC)
