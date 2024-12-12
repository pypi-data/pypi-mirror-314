import os

from pyqqq.brokerage.kis.oauth import KISAuth
from pyqqq.brokerage.kis.domestic_stock import KISDomesticStock
from pyqqq.brokerage.kis.simple import KISSimpleDomesticStock
from pyqqq.brokerage.ebest.oauth import EBestAuth
from pyqqq.brokerage.ebest.domestic_stock import EBestDomesticStock
from pyqqq.brokerage.ebest.simple import EBestSimpleDomesticStock
from pyqqq.utils.logger import get_logger


class KISConnection:
    """.env 파일에 한투 계정 정보가 있을 경우 브로커 연결을 생성"""
    logger = get_logger(__name__ + '.KISConnection')

    def __init__(self):
        app_key = os.getenv("KIS_APP_KEY")
        app_secret = os.getenv("KIS_APP_SECRET")
        account_no = os.getenv("KIS_CANO")
        account_product_code = os.getenv("KIS_ACNT_PRDT_CD")
        hts_id = os.getenv("KIS_HTS_ID")

        self.auth = KISAuth(app_key, app_secret)
        self.broker_code = 'kis'
        self.broker = KISDomesticStock(self.auth)
        self.broker_simple = KISSimpleDomesticStock(self.auth, account_no, account_product_code, hts_id)
        self.paper_auth = None
        self.paper_broker_simple = None

        self.logger.info("Connected to KIS")
        if all(k in os.environ for k in ['PAPER_KIS_APP_KEY', 'PAPER_KIS_APP_SECRET', 'PAPER_KIS_CANO', 'PAPER_KIS_ACNT_PRDT_CD']):
            self.logger.info("Using paper broker")

            paper_app_key = os.getenv("PAPER_KIS_APP_KEY")
            paper_app_secret = os.getenv("PAPER_KIS_APP_SECRET")
            paper_account_no = os.getenv("PAPER_KIS_CANO")
            paper_account_product_code = os.getenv("PAPER_KIS_ACNT_PRDT_CD")

            self.paper_auth = KISAuth(paper_app_key, paper_app_secret, paper_trading=True)
            self.paper_broker_simple = KISSimpleDomesticStock(self.paper_auth, paper_account_no, paper_account_product_code)


class EBestConnection:
    """.env 파일에 이베스트 계정 정보가 있을 경우 브로커 연결을 생성"""
    logger = get_logger(__name__ + '.EBestConnection')

    def __init__(self):
        self.auth = EBestAuth(os.getenv("EBEST_APP_KEY"), os.getenv("EBEST_APP_SECRET"))
        self.broker_code = 'ebest'
        self.broker = EBestDomesticStock(self.auth)
        self.broker_simple = EBestSimpleDomesticStock(self.auth)
        self.account_no = self.broker_simple.get_account().get('account_no')
        self.paper_auth = None
        self.paper_broker_simple = None

        self.logger.info("Connected to EBEST")
        if os.getenv("PAPER_TRADING") == "1":
            self.logger.info("Using paper broker")

            self.paper_auth = EBestAuth(os.getenv("EBEST_APP_KEY"), os.getenv("EBEST_APP_SECRET"), paper_trading=os.getenv("PAPER_TRADING") == "1")
            self.paper_broker_simple = EBestSimpleDomesticStock(self.paper_auth)


def get_base_class():
    if os.getenv("KIS_APP_KEY"):
        return KISConnection
    else:
        return EBestConnection


class PyQQQAutoConnectionSingleton(get_base_class()):
    """
    환경변수를 읽어서 자동으로 한투 또는 이베스트 브로커 연결을 생성한다.
    """
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        super().__init__()
