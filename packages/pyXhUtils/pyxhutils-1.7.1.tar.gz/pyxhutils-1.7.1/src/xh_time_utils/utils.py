import zoneinfo
import datetime as dt

time_format= '%Y-%m-%dT%H:%M:%S%z'
hktz = zoneinfo.ZoneInfo("Asia/Hong_Kong")
jptz = zoneinfo.ZoneInfo("Asia/Tokyo")
def to_time_str(d, tz=hktz, format=time_format):
    return dt.datetime(d.year,d.month,d.day,d.hour, d.minute, d.second, d.microsecond, tzinfo=tz).strftime(format)

def from_str_to_time(date_str, tz=hktz, format=time_format)->dt.datetime|None:
    return dt.datetime.strptime(date_str.replace(" +", "+"), format).replace(tzinfo=hktz) if date_str is not None else None