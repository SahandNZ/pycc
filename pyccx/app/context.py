from pyccx.constant.time_frame import TimeFrame
from pyccx.data.live_data import LiveData
from pyccx.interface.exchange import Exchange


class Context:
    def __init__(self, exchange: Exchange, symbol: str, time_frame: TimeFrame):
        self.__exchange: Exchange = exchange
        self.__symbol: str = symbol
        self.__time_frame: TimeFrame = time_frame
        self.__live_data: LiveData = LiveData(exchange=exchange, symbol=symbol, time_frame=time_frame)

    @property
    def exchange(self) -> Exchange:
        return self.__exchange

    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def time_frame(self) -> TimeFrame:
        return self.__time_frame

    @property
    def live_data(self) -> LiveData:
        return self.__live_data

    def refresh(self):
        self.__live_data.refresh()
