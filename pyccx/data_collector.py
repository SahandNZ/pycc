import math
import os
from datetime import datetime
from typing import List

from tqdm import tqdm

from pyccx.constant.time_frame import TimeFrame
from pyccx.interface.exchange import Exchange
from pyccx.interface.market import Market
from pyccx.model.candle import Candle
from pyccx.utils import create_directory


class DataCollector:
    def __init__(self, exchange: Exchange, market: Market, data_root: str, candles_count: int = None):
        self.__exchange: Exchange = exchange
        self.__market: Market = market
        self.__data_root: str = data_root
        self.__candles_count: int = candles_count

    @property
    def exchange(self) -> Exchange:
        return self.__exchange

    @property
    def market(self) -> Market:
        return self.__market

    @property
    def data_root(self) -> str:
        return self.__data_root

    @property
    def candles_count(self) -> int:
        return self.__candles_count

    def __get_candles(self, start_timestamp: int, symbol: str, time_frame: TimeFrame, show_tqdm: bool = False):
        max_candles = self.market.max_candles
        stop_timestamp = datetime.now().timestamp() // time_frame * time_frame
        candles_count = (stop_timestamp - start_timestamp) // time_frame
        requests_count = math.ceil(candles_count / max_candles)

        bar = list(range(requests_count))
        if show_tqdm:
            bar = tqdm(bar)
            bar.set_description_str(f"Downloading {symbol} {time_frame} Candles")

        candles: List[Candle] = []
        for index in bar:
            if 0 == len(candles):
                req_start = start_timestamp + index * max_candles * time_frame
                req_stop = req_start + max_candles * time_frame
            else:
                req_start = candles[-1].timestamp + time_frame
                req_stop = req_start + max_candles * time_frame

            req_candles = self.market.get_historical_candles(symbol=symbol, time_frame=time_frame,
                                                             start_timestamp=req_start, stop_timestamp=req_stop)
            candles.extend(req_candles)

        return candles

    def local_candles_path(self, symbol: str, time_frame: str) -> str:
        root = os.path.join(self.data_root, self.exchange.name, symbol)
        if not os.path.exists(root):
            create_directory(root)
        return os.path.join(root, f"{time_frame}.csv")

    def load_candles(self, symbol: str, time_frame: TimeFrame) -> List[Candle]:
        path = self.local_candles_path(symbol=symbol, time_frame=time_frame)
        local_candles = Candle.from_csv(path) if os.path.exists(path) else []
        return local_candles

    def save_candles(self, symbol: str, time_frame: TimeFrame, candles: List[Candle], mode: str):
        path = self.local_candles_path(symbol=symbol, time_frame=time_frame)
        Candle.to_csv(candles=candles, path=path, mode=mode)

    def download_candles(self, symbol: str, time_frame: TimeFrame) -> List[Candle]:
        local_candles = self.load_candles(symbol=symbol, time_frame=time_frame)

        if 0 == len(local_candles):
            stop_timestamp = datetime.now().timestamp() // time_frame * time_frame
            start_timestamp = stop_timestamp - self.candles_count * time_frame
            write_mode = 'w+'
        else:
            start_timestamp = local_candles[-1].timestamp + time_frame
            write_mode = 'a+'

        new_candles = self.__get_candles(start_timestamp=start_timestamp, symbol=symbol, time_frame=time_frame,
                                         show_tqdm=True)
        self.save_candles(symbol=symbol, time_frame=time_frame, candles=new_candles[:-1], mode=write_mode)

    def update_candles(self, symbol: str, time_frame: TimeFrame) -> List[Candle]:
        local_candles = self.load_candles(symbol=symbol, time_frame=time_frame)
        start_timestamp = local_candles[-1].timestamp + time_frame
        new_candles = self.__get_candles(start_timestamp=start_timestamp, symbol=symbol, time_frame=time_frame,
                                         show_tqdm=False)
        self.save_candles(symbol=symbol, time_frame=time_frame, candles=new_candles[:-1], mode='a+')

        live_candles = local_candles + new_candles
        return live_candles

    def download_symbols_candles(self, symbols: List[str], time_frame: TimeFrame):
        for symbol in symbols:
            self.download_candles(symbol=symbol, time_frame=time_frame)
