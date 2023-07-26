from typing import List

from pyccx.constant.hedge_mode import HedgeMode
from pyccx.constant.symbol import Symbol
from pyccx.exchanges.mexc.future.decorators import *
from pyccx.interface.https import HttpsClient
from pyccx.interface.trade import Trade
from pyccx.interface.ws import WsClient
from pyccx.model.balance import Balance
from pyccx.model.order import Order
from pyccx.model.position import Position


class MexcFutureTrade(Trade):
    def __init__(self, https: HttpsClient, ws: WsClient):
        super().__init__(https, ws)

    def post_hedge_mode(self, hedge_mode: HedgeMode):
        raise NotImplementedError()

    def get_balance(self) -> Balance:
        endpoint = "api/v1/private/account/asset/USDT"
        response = self._https.get(endpoint=endpoint, sign=True)
        balance = Balance.from_mexc(response['data'])
        return balance

    @encode_symbol
    @encode_position_side
    def get_leverage(self, symbol: Symbol, side: PositionSide) -> int:
        endpoint = "api/v1/private/position/leverage"
        params = {"symbol": symbol}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        result = [item for item in response['data'] if side == item['positionType']][0]
        leverage = int(result['leverage'])
        return leverage

    @encode_symbol
    @encode_position_side
    def post_leverage(self, symbol: Symbol, side: PositionSide, leverage: int) -> bool:
        endpoint = "api/v1/private/position/change_leverage"
        params = {"symbol": symbol, "positionType": side, "openType": 2, "leverage": leverage}
        response = self._https.post(endpoint=endpoint, params=params, sign=True)
        return response['success']

    @decode_symbol
    def get_order(self, order_id: str) -> Order:
        endpoint = f"api/v1/private/order/get/{order_id}"
        response = self._https.get(endpoint=endpoint, sign=True)
        order = Order.from_mex(response)
        return order

    def get_open_orders(self) -> List[Order]:
        pass

    @encode_symbol
    @encode_order_side
    @encode_order_type
    def post_order(self, symbol: Symbol, side: OrderSide, order_type: OrderType, volume: float,
                   price: float = None, take_profit_price: float = None, stop_loss_price: float = None) -> str:
        endpoint = "api/v1/private/order/submit"
        params = {"symbol": symbol, "side": side, "type": order_type, "openType": 2, "vol": volume, "price": price}
        response = self._https.post(endpoint=endpoint, params=params, sign=True)
        return response

    def delete_order(self, order_id: str) -> bool:
        endpoint = "api/v1/private/order/cancel"
        params = [order_id]
        response = self._https.post(endpoint=endpoint, params=params, sign=True)

    def delete_all_orders(self) -> bool:
        pass

    @encode_symbol
    def get_open_position(self, symbol: Symbol) -> Position:
        endpoint = "api/v1/private/position/open_positions"

    def get_open_positions(self) -> List[Position]:
        pass
