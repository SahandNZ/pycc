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
        pass

    def get_order(self, order_id: str) -> Order:
        pass

    def get_open_orders(self) -> List[Order]:
        pass

    def set_order(self, symbol: str, side: OrderSide, order_type: OrderType, volume: float,
                  price: float = None, take_profit_price: float = None, stop_loss_price: float = None) -> str:
        pass

    def cancel_order(self, order_id: str) -> bool:
        pass

    def cancel_all_orders(self) -> bool:
        pass

    def get_open_position(self, symbol: str) -> Position:
        pass

    def get_open_positions(self) -> List[Position]:
        pass
