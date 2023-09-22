import itertools
from typing import List, Tuple

from pyccx.constant.time_frame import TimeFrame
from pyccx.data.live_data import LiveData
from pyccx.interface.exchange import Exchange


class Context:
    def __init__(self, exchange: Exchange, symbols: List[str], time_frames: List[TimeFrame]):
        self.__exchange: Exchange = exchange
        self.__symbols: str = symbols
        self.__time_frames: TimeFrame = time_frames
        self.__pairs: List[Tuple[str, TimeFrame]] = list(itertools.product(self.symbols, self.time_frames))
        self.__live_data: LiveData = LiveData(exchange=exchange, symbols=symbols, time_frames=time_frames)

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
    def live_data(self) -> LiveData:
        return self.__live_data

    def refresh(self):
        self.__live_data.refresh()
