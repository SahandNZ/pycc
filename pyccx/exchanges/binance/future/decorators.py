from pyccx.constant.order_side import OrderSide
from pyccx.constant.order_type import OrderType
from pyccx.constant.position_side import PositionSide


def encode_symbol(func):
    def inner(*args, **kwargs):
        kwargs['symbol'] = kwargs['symbol'].replace('-', '')
        return func(*args, **kwargs)

    return inner


def encode_time_frame(func):
    def inner(*args, **kwargs):
        minute = kwargs['time_frame'] // 60
        hour = minute // 60
        day = hour // 24
        week = day // 7
        if minute < 60:
            kwargs['time_frame'] = "{}m".format(minute)
        elif hour < 24:
            kwargs['time_frame'] = "{}h".format(hour)
        elif day < 7:
            kwargs['time_frame'] = "{}d".format(day)
        elif week < 4:
            kwargs['time_frame'] = "{}w".format(week)
        else:
            kwargs['time_frame'] = "1M"

        return func(*args, **kwargs)

    return inner


def encode_order_side(func):
    def inner(*args, **kwargs):
        kwargs['side'] = 1 if OrderSide.BUY == kwargs['side'] else 2
        return func(*args, **kwargs)

    return inner


def encode_order_type(func):
    def inner(*args, **kwargs):
        kwargs['order_type'] = 5 if OrderType.MARKET == kwargs['order_type'] else kwargs['order_type']
        return func(*args, **kwargs)

    return inner


def encode_position_side(func):
    def inner(*args, **kwargs):
        kwargs['side'] = 1 if PositionSide.LONG == kwargs['side'] else 2
        return func(*args, **kwargs)

    return inner


def decode_symbol(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        if 'symbol' in result.__dict__:
            result.__dict__['symbol'] = result.__dict__['symbol'].replace('_', '-')
        return result

    return inner
