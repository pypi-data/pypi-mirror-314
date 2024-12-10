import datetime as dtm
from typing import Optional
from functools import lru_cache

from pyqqq.data import domestic
from pyqqq.utils import market_schedule
from pyqqq.utils.logger import get_logger


class DailyTickers:
    _instance = None
    _initialized = False
    logger = get_logger(__name__ + '.DailyTickers')

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self._today = dtm.date.today()
        self._date = market_schedule.get_last_trading_day()
        self._tickers = None
        self._change_date()

    def _chk_days_passed(self):
        return self._today != dtm.date.today()

    @lru_cache(maxsize=30)  # memory_profiler 로 확인 결과 하루치 fetch 결과가 약 2.5MiB
    @staticmethod
    def fetch_tickers(date):
        DailyTickers.logger.debug(f'\tfetch_tickers date={date}')
        return domestic.get_tickers(date)

    def _change_date(self, date: Optional[dtm.date] = None):
        """_tickers 가 비었거나 날짜가 바뀌었으면 새로 채워넣는다."""
        if not date:
            if self._chk_days_passed():
                self._today = dtm.date.today()
                date = market_schedule.get_last_trading_day()
            else:
                date = self._date

        if self._tickers is None or self._date != date:
            self._date = date
            self.logger.debug(f'\tdate changed. date={self._date} wait for get_tickers()')
            self._tickers = DailyTickers.fetch_tickers(self._date)

    def get_tickers(self, date: Optional[dtm.date] = None):
        """
        종목정보 가져오기
        """
        self._change_date(date)
        return self._tickers

    def get_ticker_info(self, code, date: Optional[dtm.date] = None):
        """
        종목정보 가져오기
        """
        self._change_date(date)

        # self.logger.debug(f'\tget_ticker_info code={code} date={self._date}')
        try:
            name = self._tickers.loc[code, 'name']
            type = self._tickers.loc[code, 'type']
        except KeyError:
            self.logger.error(f'KeyError on get_ticker_info. code={code}')
            return (None, None)

        return (name, type)

    def get_listing_date(self, code):
        """
        상장일 가져오기
        """
        list_date = self._tickers.loc[code, 'listing_date']
        return dtm.datetime.strptime(list_date, "%Y%m%d").date() if list_date else None
