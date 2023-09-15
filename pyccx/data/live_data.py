from datetime import datetime
from typing import List

from pyccx.constant.time_frame import TimeFrame
from pyccx.data.local_data import LocalData
from pyccx.interface.exchange import Exchange
from pyccx.interface.market import Market
from pyccx.model.candle import Candle


class LiveData:
    def __init__(self, exchange: Exchange, symbol: str, time_frame: TimeFrame):
        self.__exchange: Exchange = exchange
        self.__symbol: str = symbol
        self.__time_frame: TimeFrame = time_frame

        self.__local_data: LocalData = LocalData(exchange=exchange)
        self.__local_candles: List[Candle] = self.__local_data.download_candles(symbol=symbol, time_frame=time_frame)
        self.__live_candles: List[Candle] = None

    @property
    def exchange(self) -> Exchange:
        return self.__exchange

    @property
    def market(self) -> Market:
        return self.exchange.future.market

    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def time_frame(self) -> TimeFrame:
        return self.__time_frame

    @property
    def local_candles(self) -> List[Candle]:
        return self.__local_candles

    @property
    def candles(self) -> List[Candle]:
        return self.__live_candles

    @property
    def need_update(self) -> bool:
        current_open_timestamp = datetime.now().timestamp() // self.time_frame * self.time_frame
        return self.candles is None or self.candles[-1].timestamp < current_open_timestamp

    def update(self) -> None:
        start_timestamp = self.local_candles[-1].timestamp + self.time_frame
        new_candles = self.market.get_candles(start_timestamp=start_timestamp, symbol=self.symbol,
                                              time_frame=self.time_frame)
        self.__local_candles = self.local_candles + new_candles[:-1]
        self.__live_candles = self.local_candles + new_candles

    def refresh(self) -> None:
        if self.need_update:
            self.update()
