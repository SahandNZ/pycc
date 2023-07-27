from pyccx.exchange.bitget.future.decoder import *
from pyccx.exchange.bitget.future.encoder import *
from pyccx.interface.decorator import param_decorator


def symbol_decorator(func):
    return param_decorator(func=func, param='symbol', encoder=symbol_encoder, decoder=symbol_decoder)


def time_frame_decorator(func):
    return param_decorator(func=func, param='time_frame', encoder=time_frame_encoder, decoder=None)


def hedge_mode_decorator(func):
    return param_decorator(func=func, param='hedge_mode', encoder=hedge_mode_encoder, decoder=None)


def order_side_decorator(func):
    return param_decorator(func=func, param='side', encoder=order_side_encoder, decoder=order_side_decoder)


def order_type_decorator(func):
    return param_decorator(func=func, param='type', encoder=order_type_encoder, decoder=order_type_decoder)


def order_status_decorator(func):
    return param_decorator(func=func, param='status', encoder=None, decoder=order_status_decoder)


def position_side_decorator(func):
    return param_decorator(func=func, param='side', encoder=None, decoder=position_side_decoder)


def position_type_decorator(func):
    return param_decorator(func=func, param='type', encoder=None, decoder=position_type_decoder)
