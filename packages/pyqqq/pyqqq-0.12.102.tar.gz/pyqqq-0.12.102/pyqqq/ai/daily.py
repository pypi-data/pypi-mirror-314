import datetime
import pandas
from typing import Dict, List, Optional
import pyqqq.data.daily as daily


def get_all_ohlcv_for_date(date: datetime.date, adjusted: bool = False) -> pandas.DataFrame:
    if isinstance(date, str):
        date = datetime.date.fromisoformat(date)

    df = daily.get_all_ohlcv_for_date(date, adjusted)
    if df.empty:
        assert False, f"No OHLCV data found for {date}"
    else:
        return df


def get_ohlcv_by_codes_for_period(
    codes: List[str],
    start_date: datetime.date,
    end_date: Optional[datetime.date] = None,
    adjusted: bool = False,
    ascending: bool = False,
) -> Dict[str, pandas.DataFrame]:
    if isinstance(start_date, str):
        start_date = datetime.date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.date.fromisoformat(end_date)

    dict = daily.get_ohlcv_by_codes_for_period(codes, start_date, end_date, adjusted, ascending)
    if not dict:
        if end_date:
            assert False, f"No OHLCV data found for {start_date} to {end_date}"
        else:
            assert False, f"No OHLCV data found for {start_date}"
    else:
        return dict
