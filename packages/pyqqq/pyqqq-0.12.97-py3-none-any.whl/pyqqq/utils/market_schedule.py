"""
주식 거래소의 개장/폐장 시간을 확인하는 함수를 제공합니다.
"""

from cachetools.func import ttl_cache
from dataclasses import dataclass
from pyqqq.utils.api_client import send_request, raise_for_status
from typing import Optional
import datetime as dtm
import pyqqq.config as c
import requests


@dataclass
class MarketSchedule:
    """
    시장 운영 정보를 담고 있는 클래스입니다.
    """

    full_day_closed: bool
    """ 운영 여부 """
    exchange: str = "KRX"
    """ 시장 코드 """
    open_time: Optional[dtm.time] = None
    """ 개장 시간 """
    close_time: Optional[dtm.time] = None
    """ 폐장 시간 """
    reason: Optional[str] = None
    """ 장 운영이 중단되거나 시간이 조정된 이유 """

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if k == "_id":
                continue
            elif k in ["open_time", "close_time"] and type(v) is int:
                date = dtm.datetime.fromtimestamp(int(v / 1000))
                setattr(self, k, date.time())
            else:
                setattr(self, k, v)


def is_full_day_closed(now: Optional[dtm.datetime] = None, exchange: str = "KRX") -> bool:
    """
    주식 거래소가 휴장일인지 확인합니다.

    Args:
        now (datetime.datetime): 현재 시각. 기본값: 현재 시각
        exchange (str): 거래소 이름. 기본값: KRX

    Returns:
        bool: 휴장일 여부
    """

    assert exchange in ["KRX"], "지원하지 않는 거래소 코드입니다."

    now = dtm.datetime.now() if now is None else now

    return get_market_schedule(now.date(), exchange).full_day_closed


def is_before_opening(now: Optional[dtm.datetime] = None, exchange: str = "KRX"):
    """
    주식 거래소가 아직 개장 전인지 확인합니다.

    Args:
        now (datetime.datetime): 현재 시각. 기본값: 현재 시각
        exchange (str): 거래소 이름

    Returns:
        bool: 개장 전 여부
    """
    assert exchange in ["KRX"], "지원하지 않는 거래소 코드입니다."

    if now is None:
        now = dtm.datetime.now()

    schedule = get_market_schedule(now.date(), exchange)

    return schedule.full_day_closed or now.time() < schedule.open_time


def is_after_closing(now: Optional[dtm.datetime] = None, exchange: str = "KRX"):
    """
    주식 거래소가 이미 폐장 후인지 확인합니다.

    Args:
        now (datetime.datetime): 현재 시각. 기본값: 현재 시각
        exchange (str): 거래소 이름

    Returns:
        bool: 폐장 후 여부
    """
    assert exchange in ["KRX"], "지원하지 않는 거래소 코드입니다."

    if now is None:
        now = dtm.datetime.now()

    schedule = get_market_schedule(now.date(), exchange)
    return schedule.full_day_closed or now.time() > schedule.close_time


def is_trading_time(now: Optional[dtm.datetime] = None, exchange: str = "KRX"):
    """
    주식 거래소가 거래 시간인지 확인합니다.

    Args:
        now (datetime.datetime): 현재 시각. 기본값: 현재 시각
        exchange (str): 거래소 이름

    Returns:
        bool: 거래 시간 여부
    """
    assert exchange in ["KRX"], "지원하지 않는 거래소 코드입니다."

    return not (is_full_day_closed(now, exchange) or is_before_opening(now, exchange) or is_after_closing(now, exchange))


def get_market_schedule(date: dtm.date, exchange: str = "KRX") -> MarketSchedule:
    """
    주식 거래소의 개장/폐장 시간을 확인합니다.

    Args:
        date (datetime.date): 날짜
        exchange (str): 거래소 이름

    Returns:
        MarketSchedule: 거래소 개장/폐장 정보
    """

    full_day_closed = date.weekday() in [5, 6]

    if not full_day_closed:
        schedule = _fetch_market_scheldue(date, exchange)
        if schedule is not None:
            return MarketSchedule(**schedule.json())
        else:
            open_time = dtm.time(9, 0, 0)
            close_time = dtm.time(15, 30, 0)
            reason = None
    else:
        open_time = None
        close_time = None
        reason = "holiday"

    return MarketSchedule(exchange=exchange, full_day_closed=full_day_closed, open_time=open_time, close_time=close_time, reason=reason)


def get_last_trading_day(date: dtm.date = None) -> dtm.date:
    """
    주어진 날짜의 이전 거래일을 반환합니다.

    Args:
        date (datetime.date): 날짜. 기본값: 오늘

    Returns:
        datetime.date: 이전 거래일
    """
    if date is None:
        date = dtm.date.today()

    while True:
        date -= dtm.timedelta(days=1)
        schedule = get_market_schedule(date)
        if schedule.full_day_closed:
            continue
        else:
            return date


def get_next_trading_day(date: dtm.date = None) -> dtm.date:
    """
    주어진 날짜의 다음 거래일을 반환합니다.

    Args:
        date (datetime.date): 날짜. 기본값: 오늘

    Returns:
        datetime.date: 다음 거래일
    """
    if date is None:
        date = dtm.date.today()

    while True:
        date += dtm.timedelta(days=1)
        schedule = get_market_schedule(date)
        if schedule.full_day_closed:
            continue
        else:
            return date


def get_trading_day_with_offset(from_date: Optional[dtm.date] = None, offset_days: int = 0) -> dtm.date:
    """
    주어진 날짜로부터 주어진 오프셋만큼의 거래일을 반환합니다.

    Args:
        from_date (datetime.date): 날짜. 기본값: 오늘
        offset_days (int): 오프셋. 양수면 이후, 음수면 이전 거래일

    Returns:
        datetime.date: 거래일
    """
    if from_date is None:
        from_date = dtm.date.today()

    url = f"{c.PYQQQ_API_URL}/domestic-stock/market-schedules/KRX/trading-day"
    params = {
        "fromDate": from_date.strftime("%Y%m%d"),
        "offset": offset_days,
    }
    r = send_request("GET", url, params=params)
    raise_for_status(r)

    result = r.json()
    date = result["date"]
    return dtm.datetime.strptime(date, "%Y%m%d").date()


@ttl_cache(maxsize=1, ttl=60)
def _fetch_market_scheldue(date: dtm.date, exchange: str) -> requests.Response | None:
    url = f"{c.PYQQQ_API_URL}/domestic-stock/market-schedules/{exchange}"
    params = {"date": date}

    r = send_request("GET", url, params=params)
    if r.status_code == 404:
        return None
    else:
        raise_for_status(r)
        return r
