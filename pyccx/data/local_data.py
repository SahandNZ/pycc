import os
from datetime import datetime
from typing import List

import pandas as pd

from pyccx.constant.time_frame import TimeFrame
from pyccx.interface.exchange import Exchange
from pyccx.interface.market import Market
from pyccx.model.candle import Candle
from pyccx.utils import create_directory, resample_time_frame


class LocalData:
    def __init__(self, exchange: Exchange, data_root: str = None, candles_count: int = None):
        self.__exchange: Exchange = exchange
        self.__data_root: str = data_root
        self.__candles_count: int = candles_count

    @property
    def exchange(self) -> Exchange:
        return self.__exchange

    @property
    def market(self) -> Market:
        return self.exchange.future.market

    @property
    def data_root(self) -> str:
        return self.__data_root or os.environ.get('DATA_ROOT') or './data/'

    @property
    def candles_count(self) -> int:
        return self.__candles_count

    def _local_candles_path(self, symbol: str, time_frame: str) -> str:
        root = os.path.join(self.data_root, 'candle', self.exchange.exchange, symbol)
        if not os.path.exists(root):
            create_directory(root)
        return os.path.join(root, f"{time_frame}.csv")

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

    def download_candles(self, symbol: str, time_frame: TimeFrame) -> List[Candle]:
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
            start_timestamp = local_candles[-1].timestamp + time_frame

        # show tqdm if more than one request be sent
        show_tqdm = self.market.max_candles < (datetime.now().timestamp() - start_timestamp) // time_frame
        new_candles = self.market.get_candles(symbol, time_frame, start_timestamp, show_tqdm=show_tqdm)

        updated_candles = local_candles + new_candles[:-1]
        corrected_candles = self._check_candles(symbol=symbol, time_frame=time_frame, candles=updated_candles)
        self._save_candles(symbol=symbol, time_frame=time_frame, candles=corrected_candles)

        return corrected_candles

    def download_symbols_candles(self, symbols: List[str], time_frame: TimeFrame):
        for symbol in symbols:
            self.download_candles(symbol=symbol, time_frame=time_frame)


def load_dataframe(exchange: str, symbol: str, time_frame: TimeFrame) -> pd.DataFrame:
    ex = Exchange(exchange=exchange)
    local_data = LocalData(exchange=ex)

    one_min_candles = local_data.download_candles(symbol=symbol, time_frame=TimeFrame.MIN1)
    one_min_df = Candle.to_data_frame(candles=one_min_candles)
    df = resample_time_frame(tohlcv=one_min_df, source_timeframe=TimeFrame.MIN1, destination_timeframe=time_frame)

    return df
