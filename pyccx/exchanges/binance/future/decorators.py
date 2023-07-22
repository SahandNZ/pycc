from pyccx.constant.order_side import OrderSide
from pyccx.constant.order_type import OrderType
from pyccx.constant.position_side import PositionSide
from pyccx.constant.time_frame import TimeFrame


def encode_symbol(symbol: str) -> str:
    return symbol.replace('-', '')


def encode_time_frame(time_frame: TimeFrame) -> TimeFrame:
    minute = time_frame // 60
    hour = minute // 60
    day = hour // 24
    week = day // 7
    if minute < 60:
        return "{}m".format(minute)
    elif hour < 24:
        return "{}h".format(hour)
    elif day < 7:
        return "{}d".format(day)
    elif week < 4:
        return "{}w".format(week)
    else:
        return "1M"


def symbol_decorator(func):
    def inner(*args, **kwargs):
        kwargs['symbol'] = encode_symbol(kwargs['symbol'])
        return func(*args, **kwargs)

    return inner


def time_frame_decorator(func):
    def inner(*args, **kwargs):
        kwargs['time_frame'] = encode_time_frame(kwargs['time_frame'])
        return func(*args, **kwargs)

    return inner
