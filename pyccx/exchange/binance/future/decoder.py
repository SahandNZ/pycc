from pyccx.constant.order_side import OrderSide
from pyccx.constant.order_status import OrderStatus
from pyccx.constant.order_type import OrderType
from pyccx.constant.position_side import PositionSide
from pyccx.constant.position_type import PositionType


def symbol_decoder(symbol: str) -> str:
    return symbol.replace("USDT", "-USDT")


def order_side_decoder(order_side: str) -> int:
    return OrderSide.BUY if "buy_single" == order_side else OrderSide.SELL


def order_type_decoder(order_type: str) -> int:
    return OrderType.LIMIT if "limit" == order_type else OrderType.MARKET


def order_status_decoder(order_status: str) -> int:
    if 'new' == order_status:
        return OrderStatus.OPEN
    elif 'partially_filled' == order_status:
        return OrderStatus.PARTIALLY_FILLED
    elif 'filled' == order_status:
        return OrderStatus.FILLED
    else:
        return OrderStatus.CANCELED


def position_type_decoder(position_type: str) -> int:
    return PositionType.ISOLATED if 'fixed' == position_type else PositionType.CROSS


def position_side_decoder(position_side: str) -> int:
    return PositionSide.LONG if 'long' == position_side else PositionSide.SHORT
