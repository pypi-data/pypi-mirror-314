from typing import Optional
from pyqqq.utils.api_client import raise_for_status, send_request
from pyqqq.utils.logger import get_logger
import datetime as dtm
import pandas as pd
import numpy as np
import pyqqq.config as c


logger = get_logger(__name__)


def get_all_snapshot_for_date(date: dtm.date) -> pd.DataFrame:
    """
    전 종목 데이터를 반환합니다.

    2018년 1월 1일 데이터 부터 조회 가능합니다.

    Args:
        date (dtm.date): 조회 일자.

    Returns:
        pd.DataFrame: 전 종목의 snapshot 데이터가 포함된 pandas DataFrame.

        DataFrame의 열은 다음과 같습니다.

        - date (dtm.date): 거래일자.
        - market (str): 거래소.
        - code (str): 종목코드.
        - name (str): 종목명.
        - type (str): 종목유형.
        - change (int): 대비.
        - change_percent (float): 등락률.
        - open (int): 시가.
        - high (int): 고가.
        - low (int): 저가.
        - close (int): 종가.
        - volume (int): 거래량.
        - value (int): 거래대금.
        - market_cap (int): 시가총액.
        - shares (int): 상장주식수.
        - listing_date (dtm.datetime) 상장일.
        - days_since_listing (int): 상장 이후 경과한 일수.
        - administrative_issue (bool): 관리종목 여부.
        - alert_issue (str): 투자경고 구분.
        - fiscal_quarter_end (str): 회계분기.
        - sales_account (int): 매출액.
        - cumulative_sales_account (int): 누적 매출액.
        - operating_profit (int): 영업이익.
        - cumulative_operating_profit (int): 누적 영업이익.
        - net_income (int): 순이익.
        - cumulative_net_income (int): 누적 순이익.
        - current_assets (int): 유동자산.
        - fixed_assets (int): 고정자산.
        - total_assets (int): 자산총계.
        - flow_liabilities (int): 유동부채.
        - fixed_liabilities (int): 고정부채.
        - total_liabilities (int): 부채총계.
        - capital_stock (int): 자본금.
        - shareholders_equity (int): 자본총계.
        - retention_ratio (float): 유보율.
        - debt_ratio (float): 부채율.
        - roa (float): ROA.
        - roe (float): ROE.
        - eps (int): EPS.
        - sps (int): SPS.
        - per (float): PER.
        - pbr (float): PBR.

    Examples:
        >>> df = get_all_snapshot_for_date(dtm.datet(2020, 2, 4))
        >>> print(df.head())
                                date  market    name    type  change  ...    roe     eps       sps    per   pbr
            code                                                ...
            000020  2020-02-04   KOSPI    동화약품  EQUITY      70  ...   0.65    52.0   10684.0  21.97  0.74
            000040  2020-02-04   KOSPI   KR모터스  EQUITY       0  ... -39.20  -721.0    6670.0  -0.27  0.24
            000050  2020-02-04   KOSPI      경방  EQUITY      50  ...   0.88   171.0   12260.0  13.30  0.37
            000060  2020-02-04   KOSPI   메리츠화재  EQUITY       0  ...    NaN     NaN       NaN    NaN   NaN
            000070  2020-02-04   KOSPI   삼양홀딩스  EQUITY    -200  ...   4.85  5877.0  279735.0   7.60  0.36
            ...            ...     ...     ...     ...     ...  ...    ...     ...       ...    ...   ...
            950130  2020-02-04  KOSDAQ  엑세스바이오  EQUITY      95  ... -57.13  -577.0    1594.0 -13.25  1.63
            950140  2020-02-04  KOSDAQ   잉글우드랩  EQUITY     200  ...   3.37    76.0    6511.0 -17.88  1.69
            950160  2020-02-04  KOSDAQ  코오롱티슈진  EQUITY       0  ...    NaN     NaN       NaN    NaN   NaN
            950170  2020-02-04  KOSDAQ     JTC  EQUITY     410  ...    NaN     NaN       NaN    NaN   NaN
            950180  2020-02-04  KOSDAQ     SNK  EQUITY     -50  ...    NaN     NaN       NaN    NaN   NaN
    """

    url = f"{c.PYQQQ_API_URL}/snapshot/daily/all/{date}"
    r = send_request("GET", url)
    raise_for_status(r)

    rows = r.json()
    for data in rows:
        for iso_date in ["date", "listing_date"]:
            value = data[iso_date]
            data[iso_date] = dtm.date.fromisoformat(value)

    df = pd.DataFrame(rows)

    return _to_snapshot(df)


def get_snapshot_by_code_for_period(
    code: str,
    start_date: dtm.date,
    end_date: Optional[dtm.date] = None,
) -> pd.DataFrame:
    """
    지정된 종목과 기간에 대한 데이터를 반환합니다.

    2018년 1월 1일 데이터 부터 조회 가능합니다.

    Args:
        code (str): 조회할 주식 코드.
        start_date (dtm.date): 조회할 기간의 시작 날짜.
        end_date (Optional[dtm.date]): 조회할 기간의 종료 날짜. 지정하지 않으면 최근 거래일 까지 조회됩니다.

    Returns:
        pd.DataFrame: 전 종목의 snapshot 데이터가 포함된 pandas DataFrame.

        DataFrame의 열은 다음과 같습니다.

        - date (dtm.date): 거래일자.
        - market (str): 거래소.
        - code (str): 종목코드.
        - name (str): 종목명.
        - type (str): 종목유형.
        - change (int): 대비.
        - change_percent (float): 등락률.
        - open (int): 시가.
        - high (int): 고가.
        - low (int): 저가.
        - close (int): 종가.
        - volume (int): 거래량.
        - value (int): 거래대금.
        - market_cap (int): 시가총액.
        - shares (int): 상장주식수.
        - listing_date (dtm.datetime) 상장일.
        - days_since_listing (int): 상장 이후 경과한 일수.
        - administrative_issue (bool): 관리종목 여부.
        - alert_issue (str): 투자경고 구분.
        - fiscal_quarter_end (str): 회계분기.
        - sales_account (int): 매출액.
        - cumulative_sales_account (int): 누적 매출액.
        - operating_profit (int): 영업이익.
        - cumulative_operating_profit (int): 누적 영업이익.
        - net_income (int): 순이익.
        - cumulative_net_income (int): 누적 순이익.
        - current_assets (int): 유동자산.
        - fixed_assets (int): 고정자산.
        - total_assets (int): 자산총계.
        - flow_liabilities (int): 유동부채.
        - fixed_liabilities (int): 고정부채.
        - total_liabilities (int): 부채총계.
        - capital_stock (int): 자본금.
        - shareholders_equity (int): 자본총계.
        - retention_ratio (float): 유보율.
        - debt_ratio (float): 부채율.
        - roa (float): ROA.
        - roe (float): ROE.
        - eps (int): EPS.
        - sps (int): SPS.
        - per (float): PER.
        - pbr (float): PBR.

    Examples:
        >>> df = get_snapshot_by_code_for_period("005930", dtm.date(2018, 1, 1), dtm.date(2018, 1, 31))
        >>> print(df)
                        date market  name    type  change  ...    roe   eps    sps   per   pbr
            code                                             ...
            005930  2018-01-02  KOSPI  삼성전자  EQUITY    3000  ...  20.06  3804  30021  None  None
            005930  2018-01-03  KOSPI  삼성전자  EQUITY   30000  ...  20.06  3804  30021  None  None
            005930  2018-01-04  KOSPI  삼성전자  EQUITY  -27000  ...  20.06  3804  30021  None  None
            005930  2018-01-05  KOSPI  삼성전자  EQUITY   52000  ...  20.06  3804  30021  None  None
            005930  2018-01-08  KOSPI  삼성전자  EQUITY   -5000  ...  20.06  3804  30021  None  None
            005930  2018-01-09  KOSPI  삼성전자  EQUITY  -81000  ...  20.06  3804  30021  None  None
            005930  2018-01-10  KOSPI  삼성전자  EQUITY  -78000  ...  20.06  3804  30021  None  None
            005930  2018-01-11  KOSPI  삼성전자  EQUITY  -30000  ...  20.06  3804  30021  None  None
            005930  2018-01-12  KOSPI  삼성전자  EQUITY   -2000  ...  20.06  3804  30021  None  None
            005930  2018-01-15  KOSPI  삼성전자  EQUITY   17000  ...  20.06  3804  30021  None  None
            005930  2018-01-16  KOSPI  삼성전자  EQUITY   73000  ...  20.06  3804  30021  None  None
            005930  2018-01-17  KOSPI  삼성전자  EQUITY  -19000  ...  20.06  3804  30021  None  None
            005930  2018-01-18  KOSPI  삼성전자  EQUITY   14000  ...  20.06  3804  30021  None  None
            005930  2018-01-19  KOSPI  삼성전자  EQUITY  -29000  ...  20.06  3804  30021  None  None
            005930  2018-01-22  KOSPI  삼성전자  EQUITY  -54000  ...  20.06  3804  30021  None  None
            005930  2018-01-23  KOSPI  삼성전자  EQUITY   46000  ...  20.06  3804  30021  None  None
            005930  2018-01-24  KOSPI  삼성전자  EQUITY    9000  ...  20.06  3804  30021  None  None
            005930  2018-01-25  KOSPI  삼성전자  EQUITY   46000  ...  20.06  3804  30021  None  None
            005930  2018-01-26  KOSPI  삼성전자  EQUITY   26000  ...  20.06  3804  30021  None  None
            005930  2018-01-29  KOSPI  삼성전자  EQUITY   22000  ...  20.06  3804  30021  None  None
            005930  2018-01-30  KOSPI  삼성전자  EQUITY  -71000  ...  20.06  3804  30021  None  None
            005930  2018-01-31  KOSPI  삼성전자  EQUITY    5000  ...  20.06  3804  30021  None  None
    """

    url = f"{c.PYQQQ_API_URL}/snapshot/daily/series"
    params = {
        "code": code,
        "start_date": start_date,
    }
    if end_date is not None:
        params["end_date"] = end_date

    r = send_request("GET", url, params=params)
    raise_for_status(r)

    rows = r.json()
    for data in rows:
        for iso_date in ["date", "listing_date"]:
            value = data[iso_date]
            data[iso_date] = dtm.date.fromisoformat(value)

    df = pd.DataFrame(rows)

    return _to_snapshot(df)


def _to_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    alert = {0: None, 1: "caution", 2: "alert", 3: "risk"}

    if df.empty:
        return df

    dtypes = df.dtypes

    for k in [
        "change",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "value",
        "market_cap",
        "shares",
        "days_since_listing",
        "sales_account",
        "cumulative_sales_account",
        "operating_profit",
        "cumulative_operating_profit",
        "net_income",
        "cumulative_net_income",
        "current_assets",
        "fixed_assets",
        "total_assets",
        "flow_liabilities",
        "fixed_liabilities",
        "total_liabilities",
        "capital_stock",
        "shareholders_equity",
    ]:
        if k in dtypes:
            dtypes[k] = np.dtype("int64")

    for k in ["change_percent", "retention_ratio", "debt_ratio", "roa", "roe", "per", "pbr"]:
        if k in dtypes:
            dtypes[k] = np.dtype("float64")

    df["alert_issue"] = df["alert_issue"].apply(lambda level: alert[level])

    df = df[
        [
            "date",
            "market",
            "code",
            "name",
            "type",
            "change",
            "change_percent",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "value",
            "market_cap",
            "shares",
            "listing_date",
            "days_since_listing",
            "administrative_issue",
            "alert_issue",
            "fiscal_quarter_end",
            "sales_account",
            "cumulative_sales_account",
            "operating_profit",
            "cumulative_operating_profit",
            "net_income",
            "cumulative_net_income",
            "current_assets",
            "fixed_assets",
            "total_assets",
            "flow_liabilities",
            "fixed_liabilities",
            "total_liabilities",
            "capital_stock",
            "shareholders_equity",
            "retention_ratio",
            "debt_ratio",
            "roa",
            "roe",
            "eps",
            "sps",
            "per",
            "pbr",
        ]
    ]
    df.set_index("code", inplace=True)

    return df
