from typing import List, Dict

from pyccx.constant.hedge_mode import HedgeMode
from pyccx.exchange.bitget.future.decorator import *
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

    @hedge_mode_decorator
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

    def get_leverage(self, symbol: str) -> int:
        raise NotImplementedError()

    def post_leverage(self, symbol: str, leverage: int) -> bool:
        raise NotImplementedError()

    @symbol_decorator
    @order_side_decorator
    @order_type_decorator
    @order_status_decorator
    def get_order(self, order_id: str) -> Order:
        endpoint = "/api/mix/v1/order/detail"
        symbol = self.__oid2symbol[order_id]
        params = {"symbol": symbol, "orderId": str(order_id)}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        order = Order.from_bitget(response)
        return order

    @symbol_decorator
    @order_side_decorator
    @order_type_decorator
    @order_status_decorator
    def get_open_orders(self) -> List[Order]:
        endpoint = "/api/mix/v1/order/marginCoinCurrent"
        params = {"productType": "umcbl", "marginCoin": "USDT"}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        orders = [Order.from_bitget(item) for item in response]
        return orders

    @symbol_decorator
    @order_side_decorator
    @order_type_decorator
    def post_order(self, symbol: str, side: OrderSide, type: OrderType, volume: float, price: float = None,
                   take_profit_price: float = None, stop_loss_price: float = None) -> str:
        endpoint = "/api/mix/v1/order/placeOrder"
        params = {"symbol": symbol, "marginCoin": "USDT", "size": str(volume), "side": side, "orderType": type}
        if price is not None:
            params["price"] = str(price)
        if take_profit_price is not None:
            params["presetTakeProfitPrice"] = str(take_profit_price)
        if stop_loss_price is not None:
            params["presetStopLossPrice"] = str(stop_loss_price)
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

    def delete_all_orders(self) -> bool:
        endpoint = "/api/mix/v1/order/cancel-all-orders"
        params = {"productType": "umcbl", "marginCoin": "USDT"}
        response = self._https.post(endpoint=endpoint, params=params, sign=True)
        self.__oid2symbol = {}

    @symbol_decorator
    @position_side_decorator
    @position_type_decorator
    def get_open_position(self, symbol: str) -> Position:
        endpoint = "/api/mix/v1/position/singlePosition-v2"
        params = {"symbol": symbol, "marginCoin": "USDT"}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        position = Position.from_bitget(response)
        return position

    def get_open_positions(self) -> List[Position]:
        raise NotImplementedError()
