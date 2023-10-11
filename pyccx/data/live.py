import copy
import itertools
from datetime import datetime
from typing import List, Dict, Tuple

import pandas as pd

from pyccx.constant.time_frame import TimeFrame
from pyccx.data.local import LocalData
from pyccx.interface.exchange import Exchange
from pyccx.interface.market import Market
from pyccx.model.candle import Candle


class LiveData:
    def __init__(self, exchange: Exchange, symbols: str, time_frames: TimeFrame, data_root: str = None,
                 candles_count: int = None):
        self.__exchange: Exchange = exchange
        self.__symbols: List[str] = symbols
        self.__time_frames: List[TimeFrame] = time_frames
        self.__pairs: List[Tuple[str, TimeFrame]] = list(itertools.product(self.symbols, self.time_frames))

        self.__local_data: LocalData = LocalData(exchange=exchange, data_root=data_root, candles_count=candles_count)
        self.__local_candles_dict: Dict[Tuple[str, TimeFrame], List[Candle]] = {}
        self.__live_candles_dict: Dict[Tuple[str, TimeFrame], List[Candle]] = {}

        self._update_local_candles()

    @property
    def exchange(self) -> Exchange:
        return self.__exchange

    @property
    def market(self) -> Market:
        return self.exchange.future.market

    @property
    def symbols(self) -> List[str]:
        return self.__symbols

    @property
    def time_frames(self) -> TimeFrame:
        return self.__time_frames

    @property
    def pairs(self) -> List[Tuple[str, TimeFrame]]:
        return self.__pairs

    def get_candles(self, symbol: str, time_frame: TimeFrame) -> List[Candle]:
        return copy.deepcopy(self.__live_candles_dict[(symbol, time_frame)])

    def get_dataframe(self, symbol: str, time_frame: TimeFrame) -> pd.DataFrame:
        candles = self.__live_candles_dict[(symbol, time_frame)]
        df = Candle.to_dataframe(candles=candles)

        return df

    def get_dataframes_dict(self, symbols: List[str], time_frames: List[TimeFrame]) \
            -> Dict[Tuple[str, int], pd.DataFrame]:
        df_dict = {}
        for symbol, time_frame in itertools.product(symbols, time_frames):
            df_dict[(symbol, time_frame)] = self.get_dataframe(symbol=symbol, time_frame=time_frame)

        return df_dict

    def _update_local_candles(self):
        for symbol, time_frame in self.pairs:
            if (symbol, time_frame) not in self.__local_candles_dict:
                local_candle = self.__local_data.download_candles(symbol, time_frame)
                self.__local_candles_dict[(symbol, time_frame)] = local_candle
            else:
                local_candle = self.__local_candles_dict[(symbol, time_frame)]
                current_timestamp = datetime.now().timestamp()
                update_timestamp = local_candle[-1].timestamp + time_frame * self.market.max_candles
                if update_timestamp < current_timestamp:
                    local_candle = self.__local_data.download_candles(symbol, time_frame)
                    self.__local_candles_dict[(symbol, time_frame)] = local_candle

    def _check_live_candles(self, time_frame: TimeFrame, candles: List[Candle], last_local_candle_timestamp: int,
                            current_open_timestamp: int):
        if last_local_candle_timestamp + time_frame != candles[0].timestamp:
            raise ValueError(f"New candles has missing value at the first of the list.")

        for index in range(1, len(candles)):
            if candles[index - 1].timestamp + time_frame != candles[index].timestamp:
                raise ValueError(f"New candles has missing value at index {index}.")

        if current_open_timestamp != candles[-1].timestamp:
            raise ValueError(f"New candles has missing value at the end of the list.")

    def _update_live_candles(self):
        for symbol, time_frame in self.pairs:
            if (symbol, time_frame) not in self.__live_candles_dict:
                local_candles = self.__local_candles_dict[(symbol, time_frame)]
                self.__live_candles_dict[(symbol, time_frame)] = local_candles

            local_candles = self.__local_candles_dict[(symbol, time_frame)]
            live_candles = self.__live_candles_dict[(symbol, time_frame)]

            last_live_candle_timestamp = live_candles[-1].timestamp
            last_local_candle_timestamp = local_candles[-1].timestamp
            current_open_timestamp = datetime.now().timestamp() // time_frame * time_frame
            if last_live_candle_timestamp < current_open_timestamp:
                start_timestamp = last_local_candle_timestamp + time_frame
                new_candles = self.market.get_candles(symbol, time_frame, start_timestamp)
                self._check_live_candles(time_frame, new_candles, last_local_candle_timestamp, current_open_timestamp)
                live_candles = local_candles + new_candles
                self.__live_candles_dict[(symbol, time_frame)] = live_candles

    def refresh(self) -> None:
        self._update_local_candles()
        self._update_live_candles()
