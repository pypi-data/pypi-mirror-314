from abc import ABC
from pyqqq.backtest.broker import BaseBroker, MockBroker, TradingBroker
from pyqqq.backtest.positionprovider import BasePositionProvider
from pyqqq.backtest.wallclock import WallClock
from pyqqq.brokerage.helper import KISConnection, EBestConnection
from pyqqq.brokerage.kis.oauth import KISAuth
from pyqqq.brokerage.kis.simple_overseas import KISSimpleOverseasStock
import datetime as dtm
import os


class TradingEnvironment(ABC):
    """트레이딩 환경을 정의하는 추상 기본 클래스입니다.

    이 클래스는 트레이딩 시스템에서 사용되는 기본 환경을 정의하며,
    브로커와 시계 인스턴스를 제공하는 표준 인터페이스를 제공합니다.
    모든 구체적인 트레이딩 환경은 이 클래스를 상속받아야 합니다.
    """

    broker: BaseBroker
    """ 거래 실행을 담당하는 브로커 인스턴스 """

    clock: WallClock
    """ 시간 관리를 담당하는 시계 인스턴스 """

    def get_broker(self) -> BaseBroker:
        """현재 환경의 브로커 인스턴스를 반환합니다.

        Returns:
            BaseBroker: 거래 실행을 담당하는 브로커 인스턴스
        """
        return self.broker

    def get_clock(self) -> WallClock:
        """현재 환경의 시계 인스턴스를 반환합니다.

        Returns:
            WallClock: 시간 관리를 담당하는 시계 인스턴스
        """
        return self.clock


class BacktestEnvironment(TradingEnvironment):
    """과거 데이터를 사용한 백테스팅을 위한 거래 환경입니다.

    이 클래스는 지정된 기간 동안의 과거 데이터를 사용하여
    트레이딩 전략을 테스트할 수 있는 환경을 제공합니다.

    Example:

    .. highlight:: python
    .. code-block:: python

        env = BacktestEnvironment(
            start_time=datetime(2023, 1, 1, 9, 0),
            end_time=datetime(2023, 1, 31, 15, 30),
            time_unit="minutes"
        )
        await MyStrategy(env).run()

    """

    clock: WallClock
    """ 백테스팅용 가상 시계 인스턴스 """
    broker: MockBroker
    """ 백테스팅용 가상 브로커 인스턴스 """

    def __init__(
        self,
        start_time: dtm.datetime,
        end_time: dtm.datetime,
        time_unit: str = "minutes",
        position_provider: BasePositionProvider = None,
    ):
        """BacktestEnvironment 클래스의 초기화 메서드입니다.

        Args:
            start_time (datetime): 백테스팅 시작 시간
            end_time (datetime): 백테스팅 종료 시간
            time_unit (str, optional): 시간 단위. Defaults to "minutes".
                                    "minutes" 또는 "days" 사용 가능.
            position_provider (BasePositionProvider, optional):
                초기 포지션 정보 제공자. Defaults to None.

        Raises:
            AssertionError: start_time이 end_time보다 늦거나,
                          유효하지 않은 time_unit이 제공된 경우
        """
        super().__init__()

        assert start_time < end_time
        assert time_unit in ["minutes", "days"]

        self.clock = WallClock(live_mode=False, start_time=start_time, end_time=end_time)
        self.broker = MockBroker(self.clock, position_provider, time_unit)


class KISDomesticEnvironment(TradingEnvironment):
    """한국투자증권 API를 사용한 국내주식 거래 환경입니다.

    실제 계좌 또는 모의투자 계좌를 사용한 거래가 가능하며,
    필요한 인증 정보는 환경변수에서 가져옵니다.

    필요한 환경변수:
        - KIS_APP_KEY: API 키
        - KIS_APP_SECRET: API 시크릿
        - KIS_CANO: 계좌번호
        - KIS_ACNT_PRDT_CD: 계좌상품코드

        모의투자 사용시 추가로 필요한 환경변수:
        - PAPER_KIS_APP_KEY: 모의투자 API 키
        - PAPER_KIS_APP_SECRET: 모의투자 API 시크릿
        - PAPER_KIS_CANO: 모의투자 계좌번호
        - PAPER_KIS_ACNT_PRDT_CD: 모의투자 계좌상품코드

    Example:
        ```python
        # 실제 계좌 사용
        env = KISDomesticEnvironment(paper_trading=False)

        # 모의투자 계좌 사용
        env = KISDomesticEnvironment(paper_trading=True)
        ```
    """

    def __init__(self, paper_trading: bool = False):
        """KISDomesticEnvironment 클래스의 초기화 메서드입니다.

        Args:
            paper_trading (bool, optional): 모의투자 사용 여부. Defaults to False.
                                          True일 경우 모의투자 계좌 사용

        Raises:
            KeyError: 필요한 환경변수가 설정되지 않은 경우
        """
        conn = KISConnection()

        self.clock = WallClock(live_mode=True)
        self.broker = TradingBroker(
            data_api=conn.broker_simple,
            trading_api=conn.broker_simple if not paper_trading else conn.paper_broker_simple,
            clock=self.clock,
        )


class KISOverseasEnvironment(TradingEnvironment):
    """한국투자증권 API를 사용한 해외주식 거래 환경입니다.

    실제 계좌를 사용한 해외주식 거래가 가능하며,
    필요한 인증 정보는 환경변수에서 가져옵니다.
    현재 모의투자는 지원하지 않습니다.

    필요한 환경변수:
        - KIS_APP_KEY: API 키
        - KIS_APP_SECRET: API 시크릿
        - KIS_CANO: 계좌번호
        - KIS_ACNT_PRDT_CD: 계좌상품코드

    Example:
        ```python
        env = KISOverseasEnvironment()
        broker = env.get_broker()
        # 해외주식 거래 실행
        broker.create_order("AAPL", OrderSide.BUY, 10)
        ```
    """

    def __init__(self):
        """KISOverseasEnvironment 클래스의 초기화 메서드입니다.

        Raises:
            KeyError: 필요한 환경변수가 설정되지 않은 경우
        """
        self.clock = WallClock(live_mode=True)

        app_key = os.getenv("KIS_APP_KEY")
        app_secret = os.getenv("KIS_APP_SECRET")
        account_no = os.getenv("KIS_CANO")
        account_product_code = os.getenv("KIS_ACNT_PRDT_CD")

        auth = KISAuth(app_key, app_secret)
        simple_api = KISSimpleOverseasStock(auth, account_no, account_product_code)

        self.broker = TradingBroker(data_api=simple_api, trading_api=simple_api, clock=self.clock)


class EBestDomesticEnvironment(TradingEnvironment):
    """이베스트 API를 사용한 국내주식 거래 환경입니다.

    실제 계좌 또는 모의투자 계좌를 사용한 거래가 가능하며,
    필요한 인증 정보는 환경변수에서 가져옵니다.

    필요한 환경변수:
        - EBEST_APP_KEY: API 키
        - EBEST_APP_SECRET: API 시크릿

        모의투자 사용시 추가로 필요한 환경변수:
        - PAPER_TRADING=1

    Example:
        ```python
        # 실제 계좌 사용
        env = EBestDomesticEnvironment(paper_trading=False)

        # 모의투자 계좌 사용
        env = EBestDomesticEnvironment(paper_trading=True)
        ```
    """

    def __init__(self, paper_trading: bool = False):
        """EBestDomesticEnvironment 클래스의 초기화 메서드입니다.

        Args:
            paper_trading (bool, optional): 모의투자 사용 여부. Defaults to False.
                                          True일 경우 모의투자 계좌 사용

        Raises:
            KeyError: 필요한 환경변수가 설정되지 않은 경우
        """
        conn = EBestConnection()

        self.clock = WallClock(live_mode=True)
        self.broker = TradingBroker(
            data_api=conn.broker_simple,
            trading_api=conn.broker_simple if not paper_trading else conn.paper_broker_simple,
            clock=self.clock,
        )
