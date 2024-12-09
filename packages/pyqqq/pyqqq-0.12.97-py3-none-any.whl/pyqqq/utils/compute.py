from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP
from typing import Union


def quantize_krx_price(
    price: Union[Decimal, int, float], etf_etn: bool, rounding: str = "floor"
) -> int:
    """
    주어진 가격을 한국거래소(KRX)의 틱 사이즈에 따라 지정된 반올림 방식으로 조정합니다.

    이 함수는 ETF 또는 ETN 여부에 따라 적절한 틱 사이즈를 계산하고, 주어진 가격을 이 틱 사이즈에 맞추어 반올림합니다.
    사용자는 'round', 'ceil', 'floor' 중에서 반올림 방식을 선택할 수 있습니다.

    Args:
        price (Decimal): 반올림할 가격.
        etf_etn (bool): 가격이 ETF 또는 ETN 상품인 경우 True, 그 외는 False.
        rounding (str, optional): 반올림 방식('round', 'ceil', 'floor'). 기본값은 'floor'.

    Returns:
        int: 반올림된 가격.

    Raises:
        ValueError: rounding이 지정된 세 가지 옵션 중 하나가 아닐 경우 오류를 발생시킵니다.

    Examples:
        >>> quantize_krx_price(Decimal('1520.75'), False, 'round')
        1521
        >>> quantize_krx_price(Decimal('1520.75'), True, 'ceil')
        1521
        >>> quantize_krx_price(Decimal('1520.75'), False, 'floor')
        1520
    """

    if rounding not in ["round", "ceil", "floor"]:
        raise ValueError("rounding should be one of ['round', 'ceil', 'floor']")

    price = Decimal(price)

    constant_rounding = {
        "round": ROUND_HALF_UP,
        "ceil": ROUND_CEILING,
        "floor": ROUND_FLOOR,
    }[rounding]

    tick_size = get_krx_tick_size(price, etf_etn)

    return int(
        (price / tick_size).quantize(Decimal("1"), rounding=constant_rounding)
        * tick_size
    )


def get_krx_tick_size(price: float, etf_etn: bool) -> int:
    """
    주어진 가격과 금융 상품 유형에 따라 적절한 틱 사이즈를 반환합니다.

    한국거래소(KRX)의 틱 사이즈 규칙에 따라, 특정 가격대의 주식 또는 ETF/ETN의 최소 가격 변동 단위(틱 사이즈)를 결정합니다.
    입력된 price가 각 가격대의 최소값 미만일 경우 해당하는 틱 사이즈를 반환하며, 모든 조건에 부합하지 않는 경우 최대 가격을 반환합니다.

    Args:
        price (float): 상품의 가격.
        etf_etn (bool): 상품이 ETF 또는 ETN인 경우 True, 아니면 False.

    Returns:
        int: 결정된 틱 사이즈.

    Raises:
        AssertionError: price가 0 이하일 경우 오류를 발생시킵니다.

    Examples:
        >>> get_krx_tick_size(1500, False)
        1
        >>> get_krx_tick_size(2500, False)
        5
        >>> get_krx_tick_size(2500, True)
        1
    """

    assert price > 0, "price should be greater than 0"

    conds = []
    max_value = 0

    if etf_etn:
        conds = [(2000, 1)]
        max_value = 5
    else:
        conds = [
            (2000, 1),
            (5000, 5),
            (20000, 10),
            (50000, 50),
            (200000, 100),
            (500000, 500),
        ]
        max_value = 1000

    for min_price, size in conds:
        if price < min_price:
            return size

    return max_value
