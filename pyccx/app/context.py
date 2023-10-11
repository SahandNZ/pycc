import itertools
from typing import List, Tuple

from pyccx.constant.time_frame import TimeFrame
from pyccx.data.live import LiveData
from pyccx.interface.exchange import Exchange


class Context:
    def __init__(self, exchange: Exchange, symbols: List[str], time_frames: List[TimeFrame], data_root: str = None,
                 candles_count: int = None):
        self.__exchange: Exchange = exchange
        self.__symbols: str = symbols
        self.__time_frames: TimeFrame = time_frames
        self.__pairs: List[Tuple[str, TimeFrame]] = list(itertools.product(self.symbols, self.time_frames))
        self.__data: LiveData = LiveData(exchange=exchange, symbols=symbols, time_frames=time_frames,
                                         data_root=data_root, candles_count=candles_count)

    @property
    def exchange(self) -> Exchange:
        return self.__exchange

    @property
    def symbols(self) -> str:
        return self.__symbols

    @property
    def time_frames(self) -> TimeFrame:
        return self.__time_frames

    @property
    def pairs(self) -> List[Tuple[str, TimeFrame]]:
        return self.__pairs

    @property
    def data(self) -> LiveData:
        return self.__data

    def refresh(self):
        self.__data.refresh()
