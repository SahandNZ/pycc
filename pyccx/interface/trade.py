from abc import ABC, abstractmethod
from typing import List

from pyccx.constant.hedge_mode import HedgeMode
from pyccx.constant.order_side import OrderSide
from pyccx.constant.order_type import OrderType
from pyccx.constant.position_side import PositionSide
from pyccx.constant.symbol import Symbol
from pyccx.interface.https import HttpsClient
from pyccx.interface.ws import WsClient
from pyccx.model.balance import Balance
from pyccx.model.order import Order
from pyccx.model.position import Position


class Trade(ABC):
    def __init__(self, https: HttpsClient, ws: WsClient):
        self._https: HttpsClient = https
        self._ws: WsClient = ws

    @abstractmethod
    def post_hedge_mode(self, hedge_mode: HedgeMode):
        raise NotImplementedError()

    @abstractmethod
    def get_balance(self) -> Balance:
        raise NotImplementedError()

    @abstractmethod
    def get_leverage(self, symbol: Symbol, side: PositionSide) -> int:
        raise NotImplementedError()

    @abstractmethod
    def post_leverage(self, symbol: Symbol, side: PositionSide, leverage: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_order(self, order_id: int) -> Order:
        raise NotImplementedError()

    @abstractmethod
    def get_open_orders(self) -> List[Order]:
        raise NotImplementedError()

    @abstractmethod
    def post_order(self, symbol: Symbol, side: OrderSide, order_type: OrderType, volume: float,
                   price: float = None, take_profit_price: float = None, stop_loss_price: float = None) -> str:
        raise NotImplementedError()

    @abstractmethod
    def delete_order(self, order_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def delete_all_orders(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_open_position(self, symbol: Symbol) -> Position:
        raise NotImplementedError()

    @abstractmethod
    def get_open_positions(self) -> List[Position]:
        raise NotImplementedError()
