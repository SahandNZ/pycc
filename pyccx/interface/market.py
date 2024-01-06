import math
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Any, Callable

from pyccx.constant.time_frame import TimeFrame
from pyccx.interface.https import HttpsClient
from pyccx.interface.wss import WssClient
from pyccx.model.candle import Candle
from pyccx.model.symbol_info import SymbolInfo
from rich.progress import Progress


class Market(ABC):
    def __init__(self, https: HttpsClient, wss: WssClient):
        self._https: HttpsClient = https
        self._wss: WssClient = wss

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

    def get_candles(self, symbol: str, time_frame: TimeFrame, start_timestamp: int, stop_timestamp: int = None,
                    progress: Progress = None):
        if stop_timestamp is None:
            stop_timestamp = datetime.now().timestamp() // time_frame * time_frame + time_frame
        candles_count = (stop_timestamp - start_timestamp) // time_frame
        requests_count = math.ceil(candles_count / self.max_candles)

        items = list(range(requests_count))
        if progress is not None:
            decs = f"Downloading {symbol} {time_frame} Candles"
            task = progress.add_task(description=decs, total=len(items))

        candles: List[Candle] = []
        for index in items:
            # assign value to req_start as request start timestamp
            if 0 == len(candles):
                req_start = start_timestamp + index * self.max_candles * time_frame
            else:
                req_start = candles[-1].timestamp + time_frame

            # assign value to req_stop as request stop timestamp
            req_stop = req_start + self.max_candles * time_frame
            if stop_timestamp < req_stop:
                req_stop = stop_timestamp

            if req_start < req_stop:
                req_candles = self.get_historical_candles(symbol=symbol, time_frame=time_frame,
                                                          start_timestamp=req_start, stop_timestamp=req_stop)
                candles.extend(req_candles)

            # update progress bar
            if progress is not None:
                progress.update(task, advance=1)

        return candles

    @abstractmethod
    def subscribe_candles(self, symbol: str, time_frame: TimeFrame, on_message: Callable[[Candle], Any]):
        raise NotImplementedError()

    def join_wss(self):
        self._wss.join()
