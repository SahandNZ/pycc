from typing import List, Dict

from pyccx.constant.hedge_mode import HedgeMode
from pyccx.constant.order_side import OrderSide
from pyccx.constant.order_type import OrderType
from pyccx.constant.position_side import PositionSide
from pyccx.constant.symbol import Symbol
from pyccx.exchanges.bitget.future.decorators import *
from pyccx.interface.https import HttpsClient
from pyccx.interface.trade import Trade
from pyccx.interface.ws import WsClient
from pyccx.model.balance import Balance
from pyccx.model.order import Order
from pyccx.model.position import Position


class BitgetFutureTrade(Trade):
    def __init__(self, https: HttpsClient, ws: WsClient):
        super().__init__(https, ws)

        self.__oid2symbol: Dict[str, str] = {}

    @encode_hedge_mode
    def post_hedge_mode(self, hedge_mode: HedgeMode):
        endpoint = "/api/mix/v1/account/setPositionMode"
        params = {"productType": "umcbl", "holdMode": hedge_mode}
        response = self._https.post(endpoint=endpoint, params=params, sign=True)
        mode = HedgeMode.TWO_WAY if response['dualSidePosition'] else HedgeMode.ONE_WAY
        return mode

    def get_balance(self) -> Balance:
        endpoint = "/api/mix/v1/account/accounts"
        params = {'productType': "umcbl"}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        balance = Balance.from_bitget(response[0])
        return balance

    def get_leverage(self, symbol: Symbol, side: PositionSide) -> int:
        raise NotImplementedError()

    def post_leverage(self, symbol: Symbol, side: PositionSide, leverage: int) -> bool:
        raise NotImplementedError()

    @decode_symbol
    @decode_order_side
    @decode_order_type
    @decode_order_status
    def get_order(self, order_id: str) -> Order:
        endpoint = "/api/mix/v1/order/detail"
        symbol = self.__oid2symbol[order_id]
        params = {"symbol": symbol, "orderId": str(order_id)}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        order = Order.from_bitget(response)
        return order

    @decode_symbol
    @decode_order_side
    @decode_order_type
    @decode_order_status
    def get_open_orders(self) -> List[Order]:
        endpoint = "/api/mix/v1/order/marginCoinCurrent"
        params = {"productType": "umcbl", "marginCoin": "USDT"}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        orders = [Order.from_bitget(item) for item in response]
        return orders

    @encode_symbol
    @encode_order_side
    @encode_order_type
    def post_order(self, symbol: Symbol, side: OrderSide, order_type: OrderType, volume: float,
                   price: float = None) -> str:
        endpoint = "/api/mix/v1/order/placeOrder"
        params = {"symbol": symbol, "marginCoin": "USDT", "size": str(volume), "price": str(price), "side": side,
                  "orderType": order_type}
        response = self._https.post(endpoint=endpoint, params=params, sign=True)
        order_id = response['orderId']
        self.__oid2symbol[order_id] = symbol
        return order_id

    def delete_order(self, order_id: str) -> bool:
        endpoint = "/api/mix/v1/order/cancel-order"
        symbol = self.__oid2symbol[order_id]
        params = {"symbol": symbol, "marginCoin": "USDT", "orderId": str(order_id)}
        response = self._https.post(endpoint=endpoint, params=params, sign=True)
        order_id = response['orderId']
        del self.__oid2symbol[order_id]
        return order_id

    @encode_symbol
    @decode_symbol
    @decode_position_side
    @decode_position_type
    def get_open_position(self, symbol: Symbol) -> Position:
        endpoint = "/api/mix/v1/position/singlePosition-v2"
        params = {"symbol": symbol, "marginCoin": "USDT"}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        position = Position.from_bitget(response)
        return position

    def get_open_positions(self) -> List[Position]:
        raise NotImplementedError()
