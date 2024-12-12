from dataclasses import asdict
from decimal import Decimal
from functools import lru_cache
from pyqqq.backtest.positionprovider import BasePositionProvider
from pyqqq.backtest.wallclock import WallClock
from pyqqq.brokerage.kis.simple import KISSimpleDomesticStock
from pyqqq.brokerage.kis.simple_overseas import KISSimpleOverseasStock
from pyqqq.data.daily import get_ohlcv_by_codes_for_period as get_kr_daily_data
from pyqqq.data.minutes import get_all_day_data as get_kr_minute_data
from pyqqq.data.domestic import get_ticker_info as get_kr_ticker_info
from pyqqq.data.us_stocks import get_ticker_info as get_us_ticker_info
from pyqqq.data.us_stocks import get_all_day_data as get_us_minute_data
from pyqqq.data.us_stocks import get_ohlcv_by_codes_for_period as get_us_daily_data
from pyqqq.datatypes import *
from pyqqq.backtest.logger import Logger, get_logger
from pyqqq.utils.market_schedule import get_last_trading_day, get_market_schedule, get_trading_day_with_offset
from typing import List, Literal, Optional, Union
import datetime as dtm
import numpy as np
import os
import pandas as pd


MarketType = Literal["kr_stock", "us_stock"]


class BaseBroker:
    """브로커 인터페이스를 구현하기 위한 기본 클래스입니다.

    이 클래스는 모든 브로커 구현체가 따라야 하는 표준 인터페이스를 정의합니다.
    계좌 관리, 시장 데이터 조회, 주문 실행을 위한 메서드들을 제공합니다.
    구체적인 구현체는 모든 메서드를 오버라이드해야 합니다.

    Attributes:
        없음

    Note:
        이 클래스는 추상 기본 클래스이므로 직접 인스턴스화해서는 안 됩니다.
        모든 메서드는 NotImplementedError를 발생시키며 구체적인 하위 클래스에서 구현되어야 합니다.
    """

    def get_account(self):
        """현재 계좌 정보를 조회합니다.

        Returns:
            dict: 다음 정보를 포함하는 계좌 정보:
                - total_balance (int|Decimal): 총 평가 금액
                - purchase_amount (int|Decimal): 매입 금액
                - evaluated_amount (int|Decimal): 평가 금액
                - pnl_amount (int|Decimal): 손익 금액
                - pnl_rate (Decimal): 손익률

        Raises:
            NotImplementedError: 이 메서드는 구체적인 하위 클래스에서 구현되어야 합니다.
        """
        raise NotImplementedError

    def get_minute_price(self, code: str) -> pd.DataFrame:
        """특정 종목의 분단위 가격 데이터를 조회합니다.

        Args:
            code (str): 가격 데이터를 조회할 종목 코드

        Returns:
            pd.DataFrame: 다음 열을 포함하는 분단위 가격 데이터:
                - time (datetime): 시간
                - open (Decimal): 시가
                - high (Decimal): 고가
                - low (Decimal): 저가
                - close (Decimal): 종가
                - volume (int): 거래량

        Raises:
            NotImplementedError: 이 메서드는 구체적인 하위 클래스에서 구현되어야 합니다.
        """
        raise NotImplementedError

    def get_price(self, code: str):
        """특정 종목의 현재 가격을 조회합니다.

        Args:
            code (str): 가격을 조회할 종목 코드

        Returns:
            Decimal: 해당 종목의 현재 가격

        Raises:
            NotImplementedError: 이 메서드는 구체적인 하위 클래스에서 구현되어야 합니다.
        """
        raise NotImplementedError

    def get_daily_price(self, code: str, from_date: dtm.date, to_date: dtm.date) -> pd.DataFrame:
        """특정 기간 동안의 일별 가격 데이터를 조회합니다.

        Args:
            code (str): 가격 데이터를 조회할 종목 코드
            from_date (datetime.date): 조회 시작일 (포함)
            to_date (datetime.date): 조회 종료일 (포함)

        Returns:
            pd.DataFrame: 다음 열을 포함하는 일별 가격 데이터:
                - date (datetime): 거래일
                - open (Decimal): 시가
                - high (Decimal): 고가
                - low (Decimal): 저가
                - close (Decimal): 종가
                - volume (int): 거래량

        Raises:
            NotImplementedError: 이 메서드는 구체적인 하위 클래스에서 구현되어야 합니다.
        """
        raise NotImplementedError

    def get_pending_orders(self) -> List[StockOrder]:
        """미체결된 모든 주문을 조회합니다.

        Returns:
            List[StockOrder]: 미체결 주문 객체 리스트

        Raises:
            NotImplementedError: 이 메서드는 구체적인 하위 클래스에서 구현되어야 합니다.
        """
        raise NotImplementedError

    def get_positions(self) -> List[StockPosition]:
        """모든 종목의 현재 포지션을 조회합니다.

        Returns:
            List[StockPosition]: 현재 보유 중인 포지션을 나타내는 객체 리스트

        Raises:
            NotImplementedError: 이 메서드는 구체적인 하위 클래스에서 구현되어야 합니다.
        """
        raise NotImplementedError

    def create_order(self, asset_code: str, side: OrderSide, quantity: int, order_type: OrderType = OrderType.MARKET, price: int | Decimal = 0):
        """새로운 주문을 생성합니다.

        Args:
            asset_code (str): 주문할 종목 코드
            side (OrderSide): 매수/매도 구분
            quantity (int): 주문 수량
            order_type (OrderType, optional): 주문 타입 (기본값: MARKET)
            price (int, optional): 지정가 주문 시 주문 가격 (기본값: 0)

        Returns:
            str: 생성된 주문 번호

        Raises:
            NotImplementedError: 이 메서드는 구체적인 하위 클래스에서 구현되어야 합니다.
            ValueError: 잘못된 주문 정보가 제공된 경우
        """
        raise NotImplementedError

    def update_order(self, org_order_no: str, order_type: OrderType, price: int | Decimal, quantity: int = 0):
        """기존 주문을 수정합니다.

        Args:
            org_order_no (str): 원래 주문 번호
            order_type (OrderType): 변경할 주문 타입
            price (int): 변경할 주문 가격
            quantity (int, optional): 변경할 주문 수량 (기본값: 0, 전량)

        Returns:
            str: 새로 생성된 주문 번호

        Raises:
            NotImplementedError: 이 메서드는 구체적인 하위 클래스에서 구현되어야 합니다.
            ValueError: 잘못된 주문 정보가 제공된 경우
            Exception: 원래 주문을 찾을 수 없는 경우
        """
        raise NotImplementedError

    def cancel_order(self, order_no: str, quantity: int = 0):
        """주문을 취소합니다.

        Args:
            order_no (str): 취소할 주문 번호
            quantity (int, optional): 취소할 수량 (기본값: 0, 전량 취소)

        Raises:
            NotImplementedError: 이 메서드는 구체적인 하위 클래스에서 구현되어야 합니다.
            Exception: 취소할 주문을 찾을 수 없는 경우
        """
        raise NotImplementedError


# 모의 계좌나 실제 계좌로 트레이딩 할때 사용되는 브로커
class TradingBroker(BaseBroker):
    """실제 거래를 수행하는 브로커 클래스입니다.

    이 클래스는 실제 계좌나 모의 계좌를 통해 주식 거래를 수행합니다.
    데이터 조회용 API와 거래용 API를 분리하여 관리하며,
    KIS (한국투자증권)의 국내주식과 해외주식 API를 지원합니다.

    Note:
        - data_api와 trading_api는 서로 다른 인스턴스일 수 있으며,
          이를 통해 시세 조회와 거래를 분리하여 처리할 수 있습니다.
        - KIS의 국내주식과 해외주식 API를 모두 지원하므로,
          필요에 따라 적절한 API를 선택하여 사용할 수 있습니다.
        - 모든 거래 관련 작업은 로그로 기록되며, logging 레벨은 DEBUG로 설정됩니다.

    Example:

    .. highlight:: python
    .. code-block:: python

        # 국내주식 거래의 경우
        data_api = KISSimpleDomesticStock(...)
        trading_api = KISSimpleDomesticStock(...)
        broker = TradingBroker(data_api, trading_api)

        # 해외주식 거래의 경우
        data_api = KISSimpleOverseasStock(...)
        trading_api = KISSimpleOverseasStock(...)
        broker = TradingBroker(data_api, trading_api)

    """

    data_api: Union[KISSimpleDomesticStock, KISSimpleOverseasStock]
    """ 시세 조회 및 시장 데이터 조회를 위한 API 인터페이스 """
    trading_api: Union[KISSimpleDomesticStock, KISSimpleOverseasStock]
    """ 실제 주문 및 거래 실행을 위한 API 인터페이스 """
    logger: Logger
    """ 로깅을 위한 logger 인스턴스 """

    def __init__(
        self,
        data_api: Union[KISSimpleDomesticStock, KISSimpleOverseasStock],
        trading_api: Union[KISSimpleDomesticStock, KISSimpleOverseasStock],
        clock: WallClock,
    ):
        """TradingBroker 클래스의 초기화 메서드입니다.

        Args:
            data_api (Union[KISSimpleDomesticStock, KISSimpleOverseasStock]):
                시세 조회 및 시장 데이터 조회를 위한 API 인터페이스
            trading_api (Union[KISSimpleDomesticStock, KISSimpleOverseasStock]):
                실제 주문 및 거래 실행을 위한 API 인터페이스

        Note:
            생성된 인스턴스는 즉시 거래가 가능한 상태가 되며,
            모든 거래 관련 작업은 자동으로 로깅됩니다.
        """
        self.logger = get_logger("TradingBroker", clock)
        self.data_api = data_api
        self.trading_api = trading_api

    def get_minute_price(self, code) -> pd.DataFrame:
        return self.data_api.get_today_minute_data(code)

    def get_price(self, code):
        return self.data_api.get_price(code)

    def get_daily_price(self, code: str, from_date: dtm.date, to_date: dtm.date) -> pd.DataFrame:
        return self.data_api.get_historical_daily_data(code, from_date, to_date, adjusted=True)

    def get_orderbook(self):
        return self.data_api.get_orderbook()

    def get_account(self) -> dict:
        return self.trading_api.get_account()

    def get_pending_orders(self):
        return self.trading_api.get_pending_orders()

    def _get_pending_order(self, order_no: str) -> StockOrder | None:
        orders = self.get_pending_orders()
        return next((o for o in orders if o["order_no"] == order_no), None)

    def get_positions(self):
        return self.trading_api.get_positions()

    def create_order(self, asset_code: str, side: OrderSide, quantity: int, order_type: OrderType = OrderType.MARKET, price: int | Decimal = 0):
        return self.trading_api.create_order(asset_code, side, quantity, order_type, price)

    def update_order(self, org_order_no: str, order_type: OrderType, price: int | Decimal, quantity: int = 0):
        if isinstance(self.trading_api, KISSimpleOverseasStock):
            order = self._get_pending_order(org_order_no)
            if order is not None:
                return self.trading_api.update_order(order.asset_code, org_order_no, order_type, price, quantity)
            else:
                raise ValueError(f"order not found: {org_order_no}")
        else:
            return self.trading_api.update_order(org_order_no, order_type, price, quantity)

    def cancel_order(self, order_no: str, quantity: int = 0):
        if isinstance(self.trading_api, KISSimpleOverseasStock):
            order = self._get_pending_order(order_no)
            if order is not None:
                return self.trading_api.cancel_order(order.asset_code, order_no, quantity)
            else:
                raise ValueError(f"order not found: {order_no}")
        else:
            return self.trading_api.cancel_order(order_no, quantity)


# 백테스팅 할때 사용되는 브로커
class MockBroker(BaseBroker):
    """백테스팅을 위한 가상의 브로커 클래스입니다.

    이 클래스는 과거 데이터를 기반으로 모의 거래를 수행하고 그 결과를 분석할 수 있게 해줍니다.
    가상의 시계를 통해 시간을 제어하며, 실제 시장과 유사한 조건에서의 거래를 시뮬레이션합니다.

    특징:
        - 한국/미국 주식 시장 지원
        - 시장가/지정가/조건부지정가 주문 지원
        - 실제 거래와 동일한 수수료 체계 적용
        - 상세한 거래 이력 관리 및 분석 기능
        - 포지션 추적 및 손익 계산
        - 디버깅을 위한 상세 로깅

    Example:
        >>> # 백테스팅 환경 설정
        >>> clock = WallClock(start_date=date(2023, 1, 1))
        >>> position_provider = MyPositionProvider()
        >>> broker = MockBroker(clock, position_provider, market="kr_stock")
        >>>
        >>> # 초기 자본금 설정
        >>> broker.set_initial_cash(100_000_000)
        >>>
        >>> # 거래 실행
        >>> broker.create_order("005930", OrderSide.BUY, 100, OrderType.LIMIT, 70000)
    """

    DBG_POSTFIX = ""
    """ 디버그 파일 접미사 """
    DEBUG_FILE_PATH = "./debug"
    """ 디버그 파일 저장 경로 """
    logger: Logger
    """ 로깅을 위한 logger 인스턴스 """
    clock: WallClock
    """ 백테스팅 시간 제어를 위한 가상 시계 """
    cash: int
    """ 현재 보유 현금 """
    positions: List[StockPosition]
    """ 현재 보유 중인 포지션 목록 """
    pending_orders: List[StockOrder]
    """ 미체결 주문 목록 """
    trading_history: List[TradingHistory]
    """ 거래 이력 """
    position_provider: BasePositionProvider
    """ 초기 포지션 정보 제공자 """
    time_unit: str
    """ 거래 시간 단위 ("minutes" 또는 "days") """
    market: MarketType
    """ 거래 시장 구분 ("kr_stock" 또는 "us_stock") """

    def __init__(self, clock: WallClock, position_provider: BasePositionProvider, market: MarketType = "kr_stock", time_unit="minutes"):
        """MockBroker 클래스의 초기화 메서드입니다.

        Args:
            clock (WallClock): 백테스팅 시간을 제어할 가상 시계 객체
            position_provider: 초기 포지션 정보를 제공할 객체
            market (MarketType): 거래 시장 구분 ("kr_stock" 또는 "us_stock")
            time_unit (str, optional): 거래 시간 단위. Defaults to "minutes".
                                    "minutes" 또는 "days" 사용 가능
        """
        self.logger = get_logger("MockBroker", clock)
        self.clock = clock
        self.clock.on_time_change = self.on_time_change
        self.market = market

        self.next_order_no = 1000
        self.cash = 1_000_000_000
        self.pending_orders: List[StockOrder] = []
        self.trading_history: List[TradingHistory] = []
        self.position_provider = position_provider
        self.positions: List[StockPosition] = position_provider.get_positions(self.clock.today()) if position_provider else []
        self.time_unit = time_unit

    def set_initial_cash(self, cash):
        """초기 자본금을 설정합니다.

        Args:
            cash (int): 설정할 초기 자본금
        """
        self.cash = cash

    def increase_cash(self, amount):
        self.cash += amount

    def decrease_cash(self, amount):
        self.cash -= amount

    def get_account(self) -> dict:
        """
        계좌 요약 정보를 조회하여 총 잔고, 투자 가능 현금, 매입 금액 및 손익 정보를 반환합니다.
        """
        positions = self.get_positions()

        purchase_amount = sum([p.average_purchase_price * p.quantity for p in positions])
        evaluated_amount = sum([p.current_value for p in positions])
        pnl_amount = evaluated_amount - purchase_amount
        pnl_rate = pnl_amount / purchase_amount * 100 if purchase_amount != 0 else 0

        pending_orders = self.get_pending_orders()
        pending_amount = 0
        for order in pending_orders:
            if order.side == OrderSide.BUY:
                pending_amount += order.price * order.pending_quantity

        total_balance = self.cash + evaluated_amount + pending_amount

        return {
            "total_balance": total_balance,
            "investable_cash": self.cash,
            "purchase_amount": purchase_amount,
            "evaluated_amount": evaluated_amount,
            "pnl_amount": pnl_amount,
            "pnl_rate": pnl_rate,
        }

    def get_daily_price(self, code: str, from_date: Optional[dtm.date] = None, end_date: Optional[dtm.date] = None):
        if from_date is None:
            from_date = get_trading_day_with_offset(self.clock.today(), -10, exchange=self._get_exchange_code())
        if end_date is None:
            end_date = self.clock.today()

        if self.market == "us_stock":
            dfs = get_us_daily_data([code], from_date, end_date)
        else:
            dfs = get_kr_daily_data([code], from_date, end_date, adjusted=True, ascending=True)

        df = dfs[code]
        return df

    def get_minute_price(self, code) -> pd.DataFrame:
        df = self._get_minute_price_with_cache(self.clock.today(), code)
        if df.empty:
            return df

        return df[df.index <= self.clock.now()].copy()

    @lru_cache(maxsize=40)
    def _get_minute_price_with_cache(self, date, code) -> pd.DataFrame:
        if self.market == "us_stock":
            dfs = get_us_minute_data(date, [code])
        else:
            dfs = get_kr_minute_data(date, [code], dtm.timedelta(minutes=1), source="kis")

        df = dfs[code]
        if df.empty:
            return df

        return df

    def _get_exchange_code(self) -> str:
        """시장 일정을 조회할 때 사용하는 시장 코드를 반환합니다"""
        if self.market == "us_stock":
            return "NYSE"
        else:
            return "KRX"

    def get_price(self, code) -> int | Decimal:
        now = self.clock.now()
        today = now.date()

        def typed_result(value) -> int | Decimal:
            return Decimal(value).quantize(Decimal("0.0000")) if self.market == "us_stock" else int(value)

        schedule = get_market_schedule(today, exchange=self._get_exchange_code())
        if now.time() < schedule.open_time:
            last_trading_day = get_last_trading_day(today, exchange=self._get_exchange_code())
            if self.time_unit == "minutes":
                df = self._get_minute_price_with_cache(last_trading_day, code)
                return typed_result(df["close"].iloc[-1])
            elif self.time_unit == "days":
                df = self.get_daily_price(code, last_trading_day, last_trading_day)
                return typed_result(df["close"].iloc[-1])
            else:
                raise ValueError(f"Invalid time unit: {self.time_unit}")

        else:
            if self.time_unit == "minutes":
                df = self.get_minute_price(code)
                if not df.empty:
                    return typed_result(df["open"].iloc[-1])
                else:
                    # 현재 시간 데이터가 없을 경우 전일 종가로 대체
                    last_trading_day = get_last_trading_day(today, exchange=self._get_exchange_code())
                    df = self._get_minute_price_with_cache(last_trading_day, code)
                    return typed_result(df["close"].iloc[-1])

            elif self.time_unit == "days":
                df = self.get_daily_price(code, self.clock.today(), self.clock.today())
                return typed_result(df["close"].iloc[-1])

            else:
                raise ValueError(f"Invalid time unit: {self.time_unit}")

    def get_pending_orders(self):
        return self.pending_orders

    def get_positions(self):
        for p in self.positions:
            price = self.get_price(p.asset_code)
            p.current_price = price
            p.current_value = price * p.quantity
            p.current_pnl_value = int((price - p.average_purchase_price) * p.quantity)
            p.current_pnl = Decimal(0) if p.quantity == 0 else Decimal((p.current_pnl_value / (p.average_purchase_price * p.quantity)) * 100).quantize(Decimal("0.00"))

        positions = [p for p in self.positions if p.quantity > 0]
        return positions

    def create_order(self, asset_code: str, side: OrderSide, quantity: int, order_type: OrderType = OrderType.MARKET, price: int = 0):
        price = self.get_price(asset_code) if order_type == OrderType.MARKET else price
        self.logger.info(f"CREATE ORDER: {self._get_asset_name(asset_code)} side:{side} price:{price} quantity:{quantity} order_type:{order_type}")
        order_no = str(self.next_order_no)
        self.next_order_no += 1

        if side is OrderSide.BUY:
            total_amount = int(price * quantity)
            if self.cash < total_amount:
                raise ValueError("not enough cash")
            else:
                self.decrease_cash(total_amount)

        if isinstance(price, np.int64):
            raise ValueError(f"price must be int, not np.int64: {price} {type(price)}")

        order = StockOrder(
            order_no=order_no,
            asset_code=asset_code,
            side=side,
            price=price,
            quantity=quantity,
            filled_quantity=0,
            pending_quantity=quantity,
            order_type=order_type,
            order_time=self.clock.now(),
        )

        self.pending_orders.append(order)
        self.logger.info(f"ORDER CREATED: {order}\n{self.pending_orders}")

        return order_no

    def update_order(self, org_order_no: str, order_type: OrderType, price: int, quantity: int = 0):
        order = next((order for order in self.pending_orders if order.order_no == org_order_no), None)
        if order is None:
            raise Exception(f"order not found: {org_order_no}")

        if quantity > order.pending_quantity:
            raise ValueError("quantity must be less than pending quantity")

        if quantity == 0:
            quantity = order.pending_quantity

        if order.side == OrderSide.BUY:
            price_diff = price - order.price
            diff_value = int(price_diff * quantity)
            if self.cash < diff_value:
                raise ValueError("not enough cash")
            else:
                self.decrease_cash(diff_value)

        new_order_no = str(self.next_order_no)
        self.next_order_no += 1

        new_order = StockOrder(
            org_order_no=order.order_no,
            order_no=new_order_no,
            asset_code=order.asset_code,
            side=order.side,
            price=price,
            quantity=quantity,
            filled_quantity=0,
            pending_quantity=quantity,
            order_type=order_type,
            order_time=self.clock.now(),
        )

        order.pending_quantity -= quantity
        self.pending_orders = [o for o in self.pending_orders if o.pending_quantity > 0]
        self.pending_orders.append(new_order)

    def cancel_order(self, order_no: str, quantity: int = 0):
        order = next((order for order in self.pending_orders if order.order_no == order_no), None)
        if order is None:
            raise Exception(f"order not found: {order_no}")

        if quantity == 0:
            self.pending_orders = [o for o in self.pending_orders if o.order_no != order_no]
        else:
            order.pending_quantity -= quantity
            if order.pending_quantity == 0:
                self.pending_orders = [o for o in self.pending_orders if o.order_no != order_no]

        if order.side == OrderSide.BUY:
            if quantity == 0:
                quantity = order.pending_quantity
            self.increase_cash(int(order.price * quantity * 1.00015))

    def _cancel_order(self, order: StockOrder):
        """
        on_time_change에서 데이터 누락 등의 오류 상황일 때 미리 뺀 cash를 원복한다.
        """
        if order.side == OrderSide.BUY:
            self.increase_cash(int(order.price * order.pending_quantity))

        self.pending_orders = [o for o in self.pending_orders if o.order_no != order.order_no]

    def on_time_change(self, current_time, before_time):
        for order in list(self.pending_orders):
            if self.time_unit == "minutes":
                if current_time - before_time < dtm.timedelta(seconds=60):
                    # 강제로 1분 차이를 만들어 줌
                    before_time = current_time - dtm.timedelta(seconds=60)

                df = self.get_minute_price(order.asset_code)
                if df.empty:
                    self.logger.warning(f"ORDER CANCELED: {order.asset_code} minute data is empty")
                    self._cancel_order(order)
                    continue

                df = df[(df.index >= before_time) & (df.index < current_time)].copy()
                if df.empty:
                    self.logger.warning(f"ORDER CANCELED: {order.asset_code} minute range data is empty: {before_time} ~ {current_time}")
                    self._cancel_order(order)
                    continue

            elif self.time_unit == "days":
                from_date = before_time.date()
                to_date = current_time.date()

                df = self.get_daily_price(order.asset_code, from_date, to_date)
                if df.empty:
                    self.logger.info(f"ORDER CANCELED: {order.asset_code} daily data is empty")
                    self._cancel_order(order)
                    continue

            else:
                self._cancel_order(order)
                raise ValueError(f"Invalid time unit: {self.time_unit}")

            if df["volume"].iloc[-1] == 0:
                self.logger.info(f"ORDER CANCELED: {order.asset_code} volume is 0")
                self._cancel_order(order)
                continue

            if "cvolume" in df.columns and df["cvolume"].iloc[-1] == 0:
                self.logger.info(f"ORDER CANCELED: {order.asset_code} cvolume is 0")
                self._cancel_order(order)
                continue

            if order.order_type == OrderType.MARKET or (order.order_type == OrderType.LIMIT_CONDITIONAL and current_time.time() >= dtm.time(15, 30)):
                # 시장가 주문의 경우 주문이 제출된 시간대의 종가로 체결
                if order.order_type == OrderType.MARKET:
                    filled_price = int(df["close"].iloc[0])
                else:
                    # 조건부지정가의 미경우 미체결시 동시호가(시장종가)로 체결
                    filled_price = int(df["close"].iloc[-1])

                order.quantity = int(order.quantity)
                if order.quantity:
                    self.logger.info(f"ORDER FILLED: {order.asset_code}, price:{filled_price}, quantity:{order.quantity}, side:{order.side}, current_time:{current_time}, before_time:{before_time}")
                    if order.side == OrderSide.BUY:
                        self._buy_position(order.order_no, order.asset_code, order.quantity, filled_price)
                    else:
                        self._sell_position(order.order_no, order.asset_code, order.quantity, filled_price)

            else:
                high = int(df["high"].max())
                low = int(df["low"].min())
                close = int(df["close"].iloc[-1])

                filled_price = None

                if order.side == OrderSide.BUY:
                    if order.price > high:
                        filled_price = close
                    elif order.price < low:
                        # not fill
                        self.logger.info(f"BUY ORDER NOT FILLED: {self._get_asset_name(order.asset_code)} price:{order.price} low:{low}")
                        pass
                    else:
                        filled_price = order.price

                elif order.side == OrderSide.SELL:
                    if order.price > high:
                        # not fill
                        self.logger.info(f"SELL ORDER NOT FILLED: {self._get_asset_name(order.asset_code)} price:{order.price} high:{high}")
                        pass
                    elif order.price < low:
                        filled_price = close
                    else:
                        filled_price = order.price

                order.quantity = int(order.quantity)
                if filled_price and order.quantity:
                    filled_price = int(filled_price)
                    if order.side == OrderSide.BUY:
                        self._buy_position(order.order_no, order.asset_code, order.quantity, filled_price)
                    elif order.side == OrderSide.SELL:
                        self._sell_position(order.order_no, order.asset_code, order.quantity, filled_price)

    def _sell_position(self, order_no: str, asset_code: str, quantity: int, price: int):
        self.logger.info(f"SELL POSITION: {asset_code} price:{price} quantity:{quantity}\n{self.positions}")
        for pos in self.positions:
            if pos.asset_code == asset_code:
                pos.quantity -= quantity
                pos.quantity = max(0, pos.quantity)
                pos.sell_possible_quantity -= quantity
                pos.sell_possible_quantity = max(0, pos.sell_possible_quantity)
                pos.current_value = pos.current_price * pos.quantity
                pos.current_pnl_value = (pos.current_price - pos.average_purchase_price) * pos.quantity
                pos.current_pnl = Decimal(0) if pos.quantity == 0 else Decimal(pos.current_pnl_value / (pos.average_purchase_price * pos.quantity) * 100).quantize(Decimal("0.00"))

                sell_value = price * quantity

                # 시장별 수수료 및 세금 계산
                if self.market == "us_stock":
                    tax = 0  # 미국 주식은 매도 시 거래세 없음
                    fee = sell_value * Decimal(0.00025)  # 수수료 0.025%
                else:
                    tax = sell_value * Decimal(0.0023)  # 거래세 0.23%
                    fee = sell_value * Decimal(0.00015)  # 수수료 0.015%

                buy_value = pos.average_purchase_price * quantity
                pnl = sell_value - buy_value - fee - tax
                pnl_rate = pnl / buy_value * 100 if buy_value != 0 else 0

                self.add_trading_history(
                    TradingHistory(
                        date=self.clock.today().strftime("%Y%m%d"),
                        order_no=order_no,
                        side=OrderSide.SELL,
                        asset_code=asset_code,
                        quantity=quantity,
                        filled_price=price,
                        average_purchase_price=pos.average_purchase_price,
                        tax=tax,
                        fee=fee,
                        pnl=pnl,
                        pnl_rate=pnl_rate,
                        executed_time=int(self.clock.now().timestamp() * 1000),
                    )
                )

                self.increase_cash(sell_value - fee - tax)

        self.positions = [p for p in self.positions if p.quantity > 0]
        self.pending_orders = [o for o in self.pending_orders if o.order_no != order_no]

    def _buy_position(self, order_no: str, asset_code: str, quantity: int, price: int):
        self.logger.info(f"BUY POSITION: {asset_code} price:{price} quantity:{quantity}\n{self.positions}")
        found = False
        for pos in self.positions:
            if pos.asset_code == asset_code:
                pos.average_purchase_price = (pos.average_purchase_price * pos.quantity + price * quantity) / (pos.quantity + quantity)

                pos.quantity += quantity
                pos.sell_possible_quantity += quantity
                pos.current_value = pos.current_price * pos.quantity
                pos.current_pnl_value = (pos.current_price - pos.average_purchase_price) * pos.quantity
                pos.current_pnl = Decimal(0) if pos.quantity == 0 else Decimal(pos.current_pnl_value / (pos.average_purchase_price * pos.quantity) * 100).quantize(Decimal("0.00"))
                found = True
                break

        if not found:
            pos = StockPosition(
                asset_code=asset_code,
                asset_name=self._get_asset_name(asset_code),
                quantity=quantity,
                sell_possible_quantity=quantity,
                average_purchase_price=Decimal(price),
                current_price=price,
                current_value=price * quantity,
                current_pnl=Decimal(0),
                current_pnl_value=0,
            )
            self.positions.append(pos)

        order = next((order for order in self.pending_orders if order.order_no == order_no), None)
        order_buy_value = order.price * order.pending_quantity

        buy_value = price * quantity

        # 시장별 수수료 계산
        if self.market == "us_stock":
            fee = buy_value * Decimal(0.00025)  # 수수료 0.025%
        else:
            fee = buy_value * Decimal(0.00015)  # 수수료 0.015%

        # 주문가와 체결가가 다를 수 있음
        if order_buy_value != buy_value:
            diff_amount = order_buy_value - buy_value
            self.increase_cash(diff_amount)

        self.add_trading_history(
            TradingHistory(
                date=self.clock.today().strftime("%Y%m%d"),
                order_no=order_no,
                side=OrderSide.BUY,
                asset_code=asset_code,
                quantity=quantity,
                filled_price=price,
                average_purchase_price=Decimal(price),
                fee=fee,
                tax=0,
                pnl=0,
                pnl_rate=0,
                executed_time=int(self.clock.now().timestamp() * 1000),
            )
        )

        self.pending_orders = [o for o in self.pending_orders if o.order_no != order_no]

    def add_trading_history(self, history):
        self.trading_history.append(history)

    def show_trading_history_report(self, make_file: bool = False, filter_side: OrderSide = None):
        """거래 이력 보고서를 생성하고 표시합니다.

        Args:
            make_file (bool, optional): CSV 파일로 저장할지 여부. Defaults to False.
            filter_side (OrderSide, optional): 특정 거래 방향(매수/매도)으로 필터링. Defaults to None.

        Returns:
            dict: 거래 분석 결과를 포함하는 딕셔너리
                - count (int): 총 거래 건수
                - total_pnl (float): 총 손익률
                - avg_pnl (float): 평균 손익률
                - buy_sum (int): 총 매수 금액
                - earn_sum (int): 총 실현 손익
                - roi (float): 투자수익률 (ROI)

        Note:
            CSV 파일은 DEBUG_FILE_PATH 경로에 저장되며,
            파일명은 날짜와 시간을 포함합니다.
        """
        empty_ret = {
            "count": 0,
            "total_pnl": 0,
            "avg_pnl": 0,
            "buy_sum": 0,
            "earn_sum": 0,
            "roi": 0,
        }
        if len(self.trading_history) == 0:
            return empty_ret

        dict_list = []
        for trade in self.trading_history:
            d = asdict(trade)

            if filter_side and d["side"] != filter_side:
                continue

            d["side"] = "BUY" if d["side"] == OrderSide.BUY else "SELL"
            d["name"] = self._get_asset_name(d["asset_code"])
            d["time"] = dtm.datetime.fromtimestamp(d["executed_time"] / 1000).strftime("%Y-%m-%d %H:%M:%S")
            d["buy_value"] = d["average_purchase_price"] * d["quantity"]

            d.pop("executed_time")
            d.pop("date")
            d.pop("partial")

            d["average_purchase_price"] = d["average_purchase_price"].quantize(Decimal("0.00"))
            d["buy_value"] = int(d["buy_value"]) if d["buy_value"] else 0
            d["tax"] = int(d["tax"]) if d["tax"] else 0
            d["fee"] = int(d["fee"]) if d["fee"] else 0
            d["pnl"] = int(d["pnl"]) if d["pnl"] else 0
            d["pnl_rate"] = d["pnl_rate"].quantize(Decimal("0.00")) if d["pnl_rate"] else Decimal("0.00")

            minute_data = self.get_minute_price(d["asset_code"])
            if not minute_data.empty:
                d["max_price"] = minute_data["high"].max()
                d["max_time"] = minute_data["high"].idxmax()
                d["max_buy_rate"] = (d["max_price"] - d["average_purchase_price"]) / d["average_purchase_price"] * 100
                d["max_buy_rate"] = d["max_buy_rate"].quantize(Decimal("0.00"))
                d["min_price"] = minute_data["low"].min()
                d["min_time"] = minute_data["low"].idxmin()
            dict_list.append(d)

        df = pd.DataFrame(dict_list)
        if df.empty:
            return empty_ret

        df.set_index("time", inplace=True)
        df = df.sort_values(by="time")

        if make_file:
            df = df.sort_values(by="max_buy_rate", ascending=False)
            filename = f"{self.DEBUG_FILE_PATH}/trading_history_{self.clock.today().strftime('%Y%m%d')}_{int(dtm.datetime.now().timestamp())}_{self.DBG_POSTFIX}.csv"
            try:
                df.to_csv(filename)
            except IOError:
                os.makedirs(self.DEBUG_FILE_PATH, exist_ok=True)
                df.to_csv(filename)

        pd.set_option("display.max_rows", None)
        df = df.sort_index()
        print(df[["order_no", "side", "asset_code", "quantity", "average_purchase_price", "buy_value", "filled_price", "tax", "fee", "pnl", "pnl_rate", "name"]])
        pd.reset_option("display.max_rows")

        df.rename(
            columns={
                "order_no": "주문번호",
                "asset_code": "종목코드",
                "name": "종목명",
                "side": "매매구분",
                "quantity": "수량",
                "filled_price": "체결가",
                "average_purchase_price": "평단가",
                "buy_value": "매수금액",
                "tax": "세금",
                "fee": "수수료",
                "pnl": "손익",
                "pnl_rate": "손익률",
            },
            inplace=True,
        )
        df.index.name = "체결시간"

        # 컬럼 순서 변경
        df = df[["주문번호", "종목코드", "종목명", "매매구분", "수량", "체결가", "평단가", "매수금액", "세금", "수수료", "손익", "손익률"]]

        count = len(df)
        total_pnl = df["손익률"].sum()
        avg_pnl = df["손익률"].mean()
        buy_sum = df["매수금액"].sum()
        earn_sum = df["손익"].sum()
        roi_pnl = earn_sum / buy_sum * 100 if buy_sum != 0 else 0
        print(f"Total {count} trades, Total PnL: {total_pnl:.2f}%, Avg PnL: {avg_pnl:.2f}% ROI: {roi_pnl:>7.2f}%")
        return {
            "count": count,
            "total_pnl": total_pnl,
            "avg_pnl": avg_pnl,
            "buy_sum": buy_sum,
            "earn_sum": earn_sum,
            "roi": roi_pnl / 100,
        }

    def show_pnl_timeline(self):
        """시간별 손익 현황을 표시합니다.

        각 포지션의 시간별 가치 변화와 전체 포트폴리오의
        손익 변화를 분석하여 표시합니다.
        최대/최소 손익 시점과 금액도 함께 표시됩니다.
        """
        df = pd.DataFrame()

        for pos in self.position_provider.get_positions(self.clock.today()):
            print("Fetch minute price for", pos.asset_code)

            minute_price_df = self._get_minute_price_with_cache(self.clock.today(), pos.asset_code)
            minute_price_df.set_index("time", inplace=True)
            minute_price_df = minute_price_df.loc[: self.clock.now().replace(hour=15, minute=20, second=0, microsecond=0)].copy()

            df2 = pd.DataFrame()

            df2[f"{pos.asset_code}_current_price"] = minute_price_df["close"]
            df2[f"{pos.asset_code}_purchase_price"] = pos.average_purchase_price
            df2[f"{pos.asset_code}_quantity"] = pos.quantity
            df2[f"{pos.asset_code}_current_value"] = df2[f"{pos.asset_code}_current_price"] * pos.quantity
            df2[f"{pos.asset_code}_purchase_value"] = int(pos.average_purchase_price * pos.quantity)
            df2[f"{pos.asset_code}_pnl_value"] = df2[f"{pos.asset_code}_current_value"] - df2[f"{pos.asset_code}_purchase_value"]

            df = pd.concat([df, df2], axis=1)

        df["total_current_value"] = df.filter(like="_current_value").sum(axis=1)
        df["total_purchase_value"] = df.filter(like="_purchase_value").sum(axis=1)
        df["total_pnl_value"] = df.filter(like="_pnl_value").sum(axis=1)
        df["total_pnl_rate"] = df["total_pnl_value"] / df["total_purchase_value"] * 100

        df = df[["total_current_value", "total_purchase_value", "total_pnl_value", "total_pnl_rate"]].copy()

        if len(df) > 0:
            pd.set_option("display.max_rows", None)
            print(df)
            pd.reset_option("display.max_rows")

            print(f"- Max Pnl Time: {df['total_pnl_value'].idxmax()} {df['total_pnl_value'].max()} ({df['total_pnl_rate'].max()}%)")
            print(f"- Min Pnl Time: {df['total_pnl_value'].idxmin()} {df['total_pnl_value'].min()} ({df['total_pnl_rate'].min()}%)")

    def show_positions(self):
        """현재 보유 중인 포지션 현황을 표시합니다.

        Returns:
            dict: 포지션 분석 결과를 포함하는 딕셔너리
                - buy_value (int): 총 매수 금액
                - pnl_value (int): 총 평가 손익
                - pnl (float): 총 수익률
                - current_value (int): 현재 평가 금액
        """
        positions = [p for p in self.positions if p.quantity > 0]
        data = []
        buy_value = 0
        pnl_value = 0
        current_value = 0
        pnl = 0

        for pos in positions:
            d = asdict(pos)
            d["average_purchase_price"] = round(float(pos.average_purchase_price), 2) if pos.average_purchase_price else 0
            d["pnl_rate"] = round(float(pos.current_pnl), 2) if pos.current_pnl else 0
            d["current_pnl_value"] = int(pos.current_pnl_value)
            data.append(d)

            buy_value += d["average_purchase_price"] * d["quantity"]
            pnl_value += d["current_pnl_value"]
            current_value += d["current_value"]

        df = pd.DataFrame(data)

        if len(df) > 0:
            pnl = pnl_value / buy_value * 100 if buy_value != 0 else 0
            df = df.sort_index()
            print(df[["asset_code", "quantity", "sell_possible_quantity", "average_purchase_price", "current_price", "current_value", "current_pnl", "current_pnl_value", "pnl_rate", "asset_name"]])
            print(f"Total Buy Value: {buy_value} Total PnL: {pnl_value} ({pnl}%)")

        return {"buy_value": buy_value, "pnl_value": pnl_value, "pnl": pnl, "current_value": current_value}

    @lru_cache
    def _get_asset_name(self, code: str):
        if self.market == "us_stock":
            df = get_us_ticker_info(code)
        else:
            df = get_kr_ticker_info(code)
        return df["name"].iloc[-1]
