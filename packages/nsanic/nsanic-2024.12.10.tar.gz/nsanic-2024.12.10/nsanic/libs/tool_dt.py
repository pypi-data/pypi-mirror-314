import datetime
import time
import zoneinfo
from typing import Union

from nsanic.libs.consts import GLOBAL_TZ

MONTH_MAP = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}


def check_tz(tz: Union[str, zoneinfo.ZoneInfo] = None):
    """时区处理"""
    if tz and isinstance(tz, str):
        return zoneinfo.ZoneInfo(tz)
    return tz if tz else zoneinfo.ZoneInfo(GLOBAL_TZ)


def check_leap(year: int):
    """检查年份是否是闰年"""
    return (year % 4) if (not year % 100) else (year % 400)


def month_days(year: int, month: int):
    """获取月份里的所有天数"""
    if check_leap(year) and month == 2:
        return 29
    return MONTH_MAP.get(month)


def cur_dt(tz: Union[str, zoneinfo.ZoneInfo] = None):
    """当前日期"""
    return datetime.datetime.now(tz=check_tz(tz))


def cur_time(ms=False):
    """当前时间戳(utc)"""
    return int(time.time() * 1000) if ms else int(time.time())


def cut_utctime(ms=False):
    """当前时间戳 UTC"""
    return int(time.time()) if not ms else int(time.time() * 1000)


def dt_str(dt: Union[datetime.datetime, datetime.date, int, float, str] = None,
           fmt='%Y-%m-%d %H:%M:%S',
           tz: Union[str, zoneinfo.ZoneInfo] = None):
    """日期时间字符串格式输出, 不指定时间将输出当前时间"""
    if not dt:
        return cur_dt(tz=tz).strftime(fmt)
    if isinstance(dt, datetime.datetime):
        return dt.strftime(fmt)
    elif isinstance(dt, datetime.date):
        fmt = (fmt.replace('%H:', '').replace('%H', '').replace('%M:', '').
               replace('%M', '')).replace('%S.', '').replace('%S', '').replace('%f', '')
        return dt.strftime(fmt)
    elif isinstance(dt, (int, float)):
        dt = datetime.datetime.fromtimestamp(dt, tz=check_tz(tz))
        return dt.strftime(fmt)
    elif isinstance(dt, str):
        dt.replace('/', '-').replace('T', ' ')
        if len(dt) > 10:
            return datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S').strftime(fmt)
        return datetime.datetime.strptime(dt, '%Y-%m-%d').strftime(fmt)


def to_datetime(dt: Union[datetime.date, datetime.datetime, str, int, float],
                fmt='%Y-%m-%d %H:%M:%S', tz: Union[str, zoneinfo.ZoneInfo] = None):
    """将字符、数字等格式转化为时间日期格式"""
    if dt is None:
        return
    if isinstance(dt, str):
        dt = datetime.datetime.strptime(dt, fmt)
    if isinstance(dt, datetime.datetime):
        return dt
    elif isinstance(dt, datetime.date):
        return datetime.datetime.combine(dt, datetime.time(), tzinfo=check_tz(tz))
    elif isinstance(dt, (int, float)):
        return datetime.datetime.fromtimestamp(dt, tz=check_tz(tz))
    return


def create_dt(
        year=2023,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
        misecond=0,
        tz: Union[str, zoneinfo.ZoneInfo] = None):
    """指定创建时间日期"""
    return datetime.datetime(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second,
        microsecond=misecond, tzinfo=check_tz(tz))


def day_begin(dt: Union[datetime.datetime, datetime.date] = None, tz: Union[str, zoneinfo.ZoneInfo] = None):
    """指定时间/当天的开始时间戳 """
    if not dt:
        dt = cur_dt(tz=tz)
    if isinstance(dt, datetime.datetime):
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        return int(dt.timestamp())
    return int(datetime.datetime.combine(dt, datetime.time(), tzinfo=check_tz(tz)).timestamp())


def day_end(dt: Union[datetime.datetime, datetime.date] = None, tz: Union[str, zoneinfo.ZoneInfo] = None):
    """指定时间/当天的结束时间戳 """
    if not dt:
        dt = cur_dt(tz=tz)
    if isinstance(dt, datetime.date):
        dt = datetime.datetime.combine(dt, datetime.time(), tzinfo=check_tz(tz))
    dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    return int(dt.timestamp())


def month_begin(dt: Union[datetime.datetime, datetime.date] = None, tz: Union[str, zoneinfo.ZoneInfo] = None):
    """指定时间/当月的开始时间戳"""
    if not dt:
        dt = cur_dt(tz=tz)
    if isinstance(dt, datetime.datetime):
        dt = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return int(dt.timestamp())
    ndt = datetime.datetime.combine(dt, datetime.time(), tzinfo=check_tz(tz))
    ndt.replace(day=1)
    return int(ndt.timestamp())


def day_interval(dt: Union[datetime.datetime, datetime.date, int, float] = None,
                 tz: Union[str, zoneinfo.ZoneInfo] = None):
    """指定时间/当天的开始与结束的时间戳"""
    if not dt:
        dt = cur_dt(tz=tz)
    if isinstance(dt, (int, float)):
        dt = datetime.datetime.fromtimestamp(dt, tz=check_tz(tz))
    if isinstance(dt, datetime.date):
        dt = datetime.datetime.combine(dt, datetime.time(), tzinfo=check_tz(tz))
    s_dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    e_dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    return int(s_dt.timestamp()), int(e_dt.timestamp())


def day_hours(dt: Union[datetime.datetime, datetime.date, int, float] = None, tz: Union[str, zoneinfo.ZoneInfo] = None):
    """一天开始到结束按小时拆分的时间戳"""
    st, et = day_interval(dt, tz=tz)
    hour_list = []
    start = st
    for i in range(st, et, 3600):
        end = start + 3600 - 1
        if end >= et:
            end = et
        hour_list.append((start, end))
        start = end + 1
    return hour_list


def date_range(
        start: Union[datetime.datetime, datetime.date] = None,
        end: Union[datetime.datetime, datetime.date] = None,
        days: int = 0,
        tz: Union[str, zoneinfo.ZoneInfo] = None):
    """输出指定日期范围"""
    if isinstance(start, datetime.datetime):
        start = start.date()
    if isinstance(end, datetime.datetime):
        end = end.date()
    if start and end:
        if start > end:
            start, end = end, start
        delta = end - start
        return [start + datetime.timedelta(days=i) for i in range(delta.days + 1)]
    if start and days:
        return [start + datetime.timedelta(days=i) for i in range(days + 1)]
    if end and days:
        return [end - datetime.timedelta(days=i) for i in range(days + 1)]
    return [start] if start else ([end] if end else [cur_dt(tz=tz).date()])


def day_before(days: int, set_date: Union[datetime.datetime, datetime.date] = None, tz: Union[str, zoneinfo.ZoneInfo] = None):
    if not set_date:
        set_date = cur_dt(tz=tz)
    return (set_date - datetime.timedelta(days)) if days > 0 else (set_date + datetime.timedelta(abs(days)))
