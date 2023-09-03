from abc import ABC, abstractmethod
from typing import List

from pyccx.constant.order_side import OrderSide
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
    def get_balance(self) -> Balance:
        raise NotImplementedError()

    @abstractmethod
    def get_leverage(self, symbol: str) -> int:
        raise NotImplementedError()

    @abstractmethod
    def set_leverage(self, symbol: str, leverage: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_order(self, symbol: str, order_id: str) -> Order:
        raise NotImplementedError()

    @abstractmethod
    def get_open_orders(self, symbol: str) -> List[Order]:
        raise NotImplementedError()

    @abstractmethod
    def set_market_order(self, symbol: str, side: OrderSide, volume: float) -> str:
        raise NotImplementedError()

    @abstractmethod
    def set_limit_order(self, symbol: str, side: OrderSide, volume: float, price: float) -> str:
        raise NotImplementedError()

    @abstractmethod
    def set_stop_market_order(self, symbol: str, side: OrderSide, volume: float, stop_price: float) -> str:
        raise NotImplementedError()

    @abstractmethod
    def cancel_order(self, symbol: str, order_id: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def cancel_all_orders(self, symbol: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_open_position(self, symbol: str) -> Position:
        raise NotImplementedError()
