import datetime
import pandas
from typing import Dict, List
import pyqqq.data.minutes as minutes


def get_all_minute_data(time: datetime.datetime, source: str = "ebest", adjusted: bool = False) -> pandas.DataFrame:
    if isinstance(time, str):
        time = datetime.datetime.fromisoformat(time)

    df = minutes.get_all_minute_data(time, source, adjusted)
    if df.empty:
        assert False, f"No minute data found for {time}"
    else:
        return df


def get_all_day_data(
    date: datetime.date,
    codes: List[str] | str,
    period: datetime.timedelta = datetime.timedelta(minutes=1),
    source: str = "ebest",
    adjusted: bool = False,
    ascending: bool = True,
) -> Dict[str, pandas.DataFrame] | pandas.DataFrame:
    if isinstance(date, str):
        date = datetime.date.fromisoformat(date)

    dict = minutes.get_all_day_data(date, codes, period, source, adjusted, ascending)
    if not dict:
        assert False, f"No minute data found for {date}"
    else:
        return dict
