from typing import List

from src.constant.hedge_mode import HedgeMode
from src.constant.symbol import Symbol
from src.exchanges.binance.future.decorators import *
from src.interface.https import HttpsClient
from src.interface.trade import Trade
from src.interface.ws import WsClient
from src.model.balance import Balance
from src.model.order import Order
from src.model.position import Position


class BinanceFutureTrade(Trade):
    def __init__(self, https: HttpsClient, ws: WsClient):
        super().__init__(https, ws)

    def post_hedge_mode(self, hedge_mode: HedgeMode):
        raise NotImplementedError()

    def get_balance(self) -> Balance:
        endpoint = '/fapi/v2/balance'
        response = self._https.get(endpoint=endpoint)
        balance = Balance.from_binance([item for item in response if 'USDT' == item['asset']][0])
        return balance

    @encode_symbol
    @encode_position_side
    def get_leverage(self, symbol: Symbol, side: PositionSide) -> int:
        pass

    @encode_symbol
    @encode_position_side
    def post_leverage(self, symbol: Symbol, side: PositionSide, leverage: int) -> bool:
        pass

    @decode_symbol
    def get_order(self, order_id: str) -> Order:
        pass

    def get_open_orders(self) -> List[Order]:
        pass

    @encode_symbol
    @encode_order_side
    @encode_order_type
    def post_order(self, symbol: Symbol, side: OrderSide, order_type: OrderType, volume: float,
                   price: float = None) -> str:
        pass

    def delete_order(self, order_id: str) -> bool:
        pass

    @encode_symbol
    def get_open_position(self, symbol: Symbol) -> Position:
        pass

    def get_open_positions(self) -> List[Position]:
        pass
