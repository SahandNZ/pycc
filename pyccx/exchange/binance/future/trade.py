from typing import List

from pyccx.constant.hedge_mode import HedgeMode
from pyccx.exchange.binance.future.decorator import *
from pyccx.interface.https import HttpsClient
from pyccx.interface.trade import Trade
from pyccx.interface.ws import WsClient
from pyccx.model.balance import Balance
from pyccx.model.order import Order
from pyccx.model.position import Position


class BinanceFutureTrade(Trade):
    def __init__(self, https: HttpsClient, ws: WsClient):
        super().__init__(https, ws)

    def set_hedge_mode(self, hedge_mode: HedgeMode):
        endpoint = "/fapi/v1/positionSide/dual"
        params = {"dualSidePosition": hedge_mode == HedgeMode.TWO_WAY}
        response = self._https.post(endpoint=endpoint, params=params, sign=True)
        mode = HedgeMode.TWO_WAY if response['dualSidePosition'] else HedgeMode.ONE_WAY
        return mode

    def get_balance(self) -> Balance:
        endpoint = "/fapi/v2/balance"
        response = self._https.get(endpoint=endpoint, sign=True)
        response = [item for item in response if 'USDT' == item['asset']][0]
        balance = Balance.from_binance(response)
        return balance

    @symbol_decorator
    def get_leverage(self, symbol: str) -> int:
        endpoint = "/fapi/v2/positionRisk"
        params = {"symbol": symbol}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        leverage = response[0]['leverage']
        return leverage

    @symbol_decorator
    def set_leverage(self, symbol: str, leverage: int) -> bool:
        endpoint = "/fapi/v1/leverage"
        params = {"symbol": symbol, "leverage": leverage}
        response = self._https.post(endpoint=endpoint, params=params, sign=True)
        leverage = response['leverage']
        return leverage

    @symbol_decorator
    @order_side_decorator
    @order_type_decorator
    @order_status_decorator
    def get_order(self, symbol: str, order_id: str) -> Order:
        endpoint = "/fapi/v1/openOrders"
        params = {"symbol": symbol, "orderId": order_id}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        orders = Order.from_binance(response)
        return orders

    @symbol_decorator
    @order_side_decorator
    @order_type_decorator
    @order_status_decorator
    def get_open_orders(self, symbol: str) -> List[Order]:
        endpoint = "/fapi/v1/openOrders"
        params = {"symbol": symbol}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        orders = [Order.from_binance(item) for item in response]
        return orders

    @symbol_decorator
    @order_side_decorator
    def set_market_order(self, symbol: str, side: OrderSide, volume: float) -> str:
        endpoint = "/fapi/v1/order"
        params = {"symbol": symbol, "side": side, "type": "MARKET", "quantity": volume}
        response = self._https.post(endpoint=endpoint, params=params, sign=True)
        order_id = response["orderId"]
        return order_id

    @symbol_decorator
    @order_side_decorator
    def set_limit_order(self, symbol: str, side: OrderSide, volume: float, price: float) -> str:
        endpoint = "/fapi/v1/order"
        params = {"symbol": symbol, "side": side, "type": "LIMIT", "quantity": volume, "price": price}
        response = self._https.post(endpoint=endpoint, params=params, sign=True)
        order_id = response["orderId"]
        return order_id

    @symbol_decorator
    @order_side_decorator
    def set_stop_market_order(self, symbol: str, side: OrderSide, volume: float, stop_price: float) -> str:
        endpoint = "/fapi/v1/order"
        params = {"symbol": symbol, "side": side, "type": "LIMIT", "quantity": volume, "stopPrice": stop_price}
        response = self._https.post(endpoint=endpoint, params=params, sign=True)
        order_id = response["orderId"]
        return order_id

    def cancel_order(self, symbol: str, order_id: str) -> bool:
        endpoint = "/fapi/v1/order"
        params = {"symbol": symbol, "orderId": order_id}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        return True

    def cancel_all_orders(self, symbol: str) -> bool:
        endpoint = "/fapi/v1/allOpenOrders"
        params = {"symbol": symbol}
        response = self._https.get(endpoint=endpoint, params=params, sign=True)
        return True

    def get_open_position(self, symbol: str) -> Position:
        pass
