from src.constant.order_side import OrderSide
from src.constant.order_type import OrderType
from src.constant.position_side import PositionSide


def encode_symbol(func):
    def inner(*args, **kwargs):
        kwargs['symbol'] = kwargs['symbol'].replace('-', '_')
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
