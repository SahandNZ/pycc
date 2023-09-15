import math
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from tqdm import tqdm

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
    def get_symbol_info(self, symbol: str) -> SymbolInfo:
        raise NotImplementedError()

    @abstractmethod
    def get_recent_candles(self, symbol: str, time_frame: TimeFrame) -> List[Candle]:
        raise NotImplementedError()

    @abstractmethod
    def get_historical_candles(self, symbol: str, time_frame: TimeFrame, start_timestamp: int, stop_timestamp) -> \
            List[Candle]:
        raise NotImplementedError()

    def get_candles(self, start_timestamp: int, symbol: str, time_frame: TimeFrame, show_tqdm: bool = False):
        stop_timestamp = datetime.now().timestamp() // time_frame * time_frame
        candles_count = (stop_timestamp - start_timestamp) // time_frame
        requests_count = math.ceil(candles_count / self.max_candles)

        bar = list(range(requests_count))
        if show_tqdm:
            bar = tqdm(bar)
            bar.set_description_str(f"Downloading {symbol} {time_frame} Candles")

        candles: List[Candle] = []
        for index in bar:
            if 0 == len(candles):
                req_start = start_timestamp + index * self.max_candles * time_frame
                req_stop = req_start + self.max_candles * time_frame
            else:
                req_start = candles[-1].timestamp + time_frame
                req_stop = req_start + self.max_candles * time_frame

            req_candles = self.get_historical_candles(symbol=symbol, time_frame=time_frame,
                                                      start_timestamp=req_start, stop_timestamp=req_stop)
            candles.extend(req_candles)

        return candles
