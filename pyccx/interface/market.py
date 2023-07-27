from abc import ABC, abstractmethod
from typing import List

from pyccx.constant.time_frame import TimeFrame
from pyccx.interface.https import HttpsClient
from pyccx.interface.ws import WsClient
from pyccx.model.candle import Candle
from pyccx.model.symbol_info import SymbolInfo


class Market(ABC):
    def __init__(self, https: HttpsClient, ws: WsClient):
        self._https: HttpsClient = https
        self._ws: WsClient = ws

    @property
    @abstractmethod
    def max_candles(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_server_time(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_ping(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def get_symbols_info(self) -> List[SymbolInfo]:
        raise NotImplementedError()

    @abstractmethod
    def get_candles(self, symbol: str, time_frame: TimeFrame) -> List[Candle]:
        raise NotImplementedError()

    @abstractmethod
    def get_historical_candles(self, symbol: str, time_frame: TimeFrame, start_timestamp: int, stop_timestamp) -> \
            List[Candle]:
        raise NotImplementedError()
