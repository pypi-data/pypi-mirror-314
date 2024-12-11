from dataclasses import asdict
from enum import Enum

from xh_time_utils import to_time_str
import datetime as dt

def custom_asdict_factory(data):
    def convert_value(obj):
        if isinstance(obj, dt.datetime):
            # return obj.astimezone(hktz).strftime(time_format)
            return to_time_str(obj)
        elif isinstance(obj, Enum):
            return obj.name
        return obj

    return dict((k, convert_value(v)) for k, v in data)

class SimpleDataClass:
    def dict(self) -> dict:
        return asdict(self, dict_factory=custom_asdict_factory)
