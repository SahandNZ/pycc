import itertools
from datetime import datetime
from typing import List, Dict, Tuple

from pyccx.constant.time_frame import TimeFrame
from pyccx.data.local_data import LocalData
from pyccx.interface.exchange import Exchange
from pyccx.interface.market import Market
from pyccx.model.candle import Candle


class LiveData:
    def __init__(self, exchange: Exchange, symbols: str, time_frames: TimeFrame):
        self.__exchange: Exchange = exchange
        self.__symbols: List[str] = symbols
        self.__time_frames: List[TimeFrame] = time_frames
        self.__pairs: List[Tuple[str, TimeFrame]] = list(itertools.product(self.symbols, self.time_frames))

        self.__local_data: LocalData = LocalData(exchange=exchange)
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
        return self.__live_candles_dict[(symbol, time_frame)]

    def _update_local_candles(self):
        for symbol, time_frame in self.pairs:
            if (symbol, time_frame) not in self.__local_candles_dict:
                local_candle = self.__local_data.get_candles(symbol, time_frame)
                self.__local_candles_dict[(symbol, time_frame)] = local_candle
            else:
                local_candle = self.__local_candles_dict[(symbol, time_frame)]
                current_timestamp = datetime.now().timestamp()
                update_timestamp = local_candle[-1].timestamp + time_frame * self.market.max_candles
                if update_timestamp < current_timestamp:
                    local_candle = self.__local_data.get_candles(symbol, time_frame)
                    self.__local_candles_dict[(symbol, time_frame)] = local_candle

    def _update_live_candles(self):
        for symbol, time_frame in self.pairs:
            if (symbol, time_frame) not in self.__live_candles_dict:
                local_candles = self.__local_candles_dict[(symbol, time_frame)]
                self.__live_candles_dict[(symbol, time_frame)] = local_candles

            local_candles = self.__local_candles_dict[(symbol, time_frame)]
            live_candles = self.__live_candles_dict[(symbol, time_frame)]

            last_live_candle_timestamp = live_candles[-1].timestamp
            current_open_timestamp = datetime.now().timestamp() // time_frame * time_frame
            if last_live_candle_timestamp < current_open_timestamp:
                new_candles = self.market.get_candles(symbol, time_frame, current_open_timestamp)
                updated_live_candles = local_candles + new_candles
                self.__live_candles_dict[(symbol, time_frame)] = updated_live_candles

    def refresh(self) -> None:
        self._update_local_candles()
        self._update_live_candles()
