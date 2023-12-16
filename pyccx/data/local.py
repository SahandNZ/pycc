import itertools
import os
from datetime import datetime
from typing import List, Dict, Tuple

import pandas as pd
from tqdm import tqdm

from pyccx.constant.time_frame import TimeFrame
from pyccx.defaults import DATA_ROOT, BASE_TIME_FRAME
from pyccx.interface.exchange import Exchange
from pyccx.interface.market import Market
from pyccx.model.candle import Candle
from pyccx.utils import create_directory, resample_time_frame


class LocalData:
    def __init__(self, exchange: Exchange, candles_count: int = None):
        self.__exchange: Exchange = exchange
        self.__candles_count: int = candles_count

    @property
    def exchange(self) -> Exchange:
        return self.__exchange

    @property
    def market(self) -> Market:
        return self.exchange.future.market

    @property
    def directory(self) -> str:
        return os.path.join(DATA_ROOT, "candle")

    @property
    def candles_count(self) -> int:
        return self.__candles_count

    def _local_candles_path(self, symbol: str, time_frame: str) -> str:
        exchange_symbol_directory = os.path.join(self.directory, self.exchange.exchange, symbol)
        create_directory(exchange_symbol_directory)
        file_path = os.path.join(exchange_symbol_directory, f"{time_frame}.csv")

        return file_path

    def _load_candles(self, symbol: str, time_frame: TimeFrame) -> List[Candle]:
        path = self._local_candles_path(symbol=symbol, time_frame=time_frame)
        local_candles = Candle.from_csv(path) if os.path.exists(path) else []
        return local_candles

    def _refine_candles(self, symbol: str, time_frame: TimeFrame, candles: List[Candle], index: int) -> List[Candle]:
        start_timestamp = candles[index - 1].timestamp + time_frame
        stop_timestamp = candles[index].timestamp
        leftover_candles = self.market.get_candles(symbol, time_frame, start_timestamp, stop_timestamp=stop_timestamp)

        corrected_candles = candles[:index] + leftover_candles + candles[index:]
        return self._check_candles(symbol, time_frame, corrected_candles)

    def _check_candles(self, symbol: str, time_frame: TimeFrame, candles: List[Candle]) -> List[Candle]:
        for index in range(1, len(candles)):
            if candles[index - 1].timestamp + time_frame != candles[index].timestamp:
                return self._refine_candles(symbol, time_frame, candles, index)

        return candles

    def _save_candles(self, symbol: str, time_frame: TimeFrame, candles: List[Candle], mode: str = 'w+'):
        path = self._local_candles_path(symbol=symbol, time_frame=time_frame)
        Candle.to_csv(candles=candles, path=path, mode=mode)

    def download_candles(self, symbol: str, time_frame: TimeFrame, update: bool = True) -> List[Candle]:
        local_candles = self._load_candles(symbol=symbol, time_frame=time_frame)

        # assign value to start timestamp
        if 0 == len(local_candles):
            if self.candles_count is None:
                symbol_info = self.market.get_symbol_info(symbol=symbol)
                start_timestamp = symbol_info.on_board_timestamp
            else:
                current_open_timestamp = datetime.now().timestamp() // time_frame * time_frame
                start_timestamp = current_open_timestamp - self.candles_count * time_frame
        else:
            start_timestamp = local_candles[-1].timestamp + time_frame if update else None

        if start_timestamp is not None:
            # show tqdm if more than one request be sent
            show_tqdm = self.market.max_candles < (datetime.now().timestamp() - start_timestamp) // time_frame
            new_candles = self.market.get_candles(symbol, time_frame, start_timestamp, show_tqdm=show_tqdm)

            updated_candles = local_candles + new_candles[:-1]
            corrected_candles = self._check_candles(symbol=symbol, time_frame=time_frame, candles=updated_candles)
            self._save_candles(symbol=symbol, time_frame=time_frame, candles=corrected_candles)

            local_candles = corrected_candles

        return local_candles

    def download_symbols_candles(self, symbols: List[str], time_frame: TimeFrame):
        for symbol in symbols:
            self.download_candles(symbol=symbol, time_frame=time_frame)

    def load_dataframe(self, symbol: str, time_frame: TimeFrame) -> pd.DataFrame:
        path = self._local_candles_path(symbol=symbol, time_frame=time_frame)
        local_dataframe = Candle.load_dataframe(path)
        return local_dataframe


__EXCHANGE: Exchange = None
__LOCAL_DATA: LocalData = None


def load_dataframe(exchange: str, symbol: str, time_frame: TimeFrame, update: bool = False,
                   proxies: Dict[str, str] = None) -> pd.DataFrame:
    global __EXCHANGE
    global __LOCAL_DATA
    if __EXCHANGE is None or __EXCHANGE.exchange != exchange:
        __EXCHANGE = Exchange(exchange=exchange, proxies=proxies)
        __LOCAL_DATA = LocalData(exchange=__EXCHANGE)

    if update:
        candles = __LOCAL_DATA.download_candles(symbol=symbol, time_frame=BASE_TIME_FRAME, update=update)
        sdf = Candle.to_dataframe(candles=candles)
    else:
        sdf = __LOCAL_DATA.load_dataframe(symbol=symbol, time_frame=BASE_TIME_FRAME)

    df = resample_time_frame(tohlcv=sdf, source_timeframe=BASE_TIME_FRAME, destination_timeframe=time_frame)

    return df


def load_dataframes_dict(exchange: str, symbols: List[str], time_frames: List[TimeFrame], update: bool = False,
                         proxies: Dict[str, str] = None) -> Dict[Tuple[str, int], pd.DataFrame]:
    dfs_dict = {}
    bar = tqdm(list(itertools.product(symbols, time_frames)))
    bar.set_description_str("Loading Dataframes")
    for symbol, time_frame in bar:
        df = load_dataframe(exchange=exchange, symbol=symbol, time_frame=time_frame, update=update, proxies=proxies)
        dfs_dict[(symbol, time_frame)] = df

    return dfs_dict
