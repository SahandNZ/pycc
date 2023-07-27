from typing import List

from pyccx.constant.hedge_mode import HedgeMode
from pyccx.constant.symbol import Symbol
from pyccx.exchange.binance.future.decorators import *
from pyccx.interface.https import HttpsClient
from pyccx.interface.trade import Trade
from pyccx.interface.ws import WsClient
from pyccx.model.balance import Balance
from pyccx.model.order import Order
from pyccx.model.position import Position


class BinanceFutureTrade(Trade):
    def __init__(self, https: HttpsClient, ws: WsClient):
        super().__init__(https, ws)

    def post_hedge_mode(self, hedge_mode: HedgeMode):
        pass

    def get_balance(self) -> Balance:
        pass

    def get_leverage(self, symbol: Symbol) -> int:
        pass

    def post_leverage(self, symbol: Symbol, leverage: int) -> bool:
        pass

    def get_order(self, order_id: str) -> Order:
        pass

    def get_open_orders(self) -> List[Order]:
        pass

    def post_order(self, symbol: Symbol, side: OrderSide, order_type: OrderType, volume: float,
                   price: float = None, take_profit_price: float = None, stop_loss_price: float = None) -> str:
        pass

    def delete_order(self, order_id: str) -> bool:
        pass

    def delete_all_orders(self) -> bool:
        pass

    def get_open_position(self, symbol: Symbol) -> Position:
        pass

    def get_open_positions(self) -> List[Position]:
        pass
