import datetime
import pandas
from typing import List
import pyqqq.data.domestic as domestic


def get_market_cap(date: datetime.date) -> pandas.DataFrame:
    if isinstance(date, str):
        date = datetime.date.fromisoformat(date)

    df = domestic.get_market_cap(date)
    if not df.empty:
        df.rename(columns={"value": "market_cap"}, inplace=True)

    return df


def get_market_cap_by_codes(codes: List[str], date: datetime.date = None) -> pandas.DataFrame:
    if isinstance(date, str):
        date = datetime.date.fromisoformat(date)

    df = domestic.get_market_cap_by_codes(codes, date)
    if not df.empty:
        df.rename(columns={"value": "market_cap"}, inplace=True)

    return df
