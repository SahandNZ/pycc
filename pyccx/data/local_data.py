import os
from typing import List

from pyccx.constant.time_frame import TimeFrame
from pyccx.interface.exchange import Exchange
from pyccx.interface.market import Market
from pyccx.model.candle import Candle
from pyccx.utils import create_directory


class LocalData:
    def __init__(self, exchange: Exchange, data_root: str = None):
        self.__exchange: Exchange = exchange
        self.__data_root: str = data_root

    @property
    def exchange(self) -> Exchange:
        return self.__exchange

    @property
    def market(self) -> Market:
        return self.exchange.future.market

    @property
    def data_root(self) -> str:
        return self.__data_root or os.environ.get('DATA_ROOT') or '~/data/'

    def _local_candles_path(self, symbol: str, time_frame: str) -> str:
        root = os.path.join(self.data_root, self.exchange.name, symbol)
        if not os.path.exists(root):
            create_directory(root)
        return os.path.join(root, f"{time_frame}.csv")

    def _load_candles(self, symbol: str, time_frame: TimeFrame) -> List[Candle]:
        path = self._local_candles_path(symbol=symbol, time_frame=time_frame)
        local_candles = Candle.from_csv(path) if os.path.exists(path) else []
        return local_candles

    # TODO
    def _refine_candles(self, symbol: str, time_frame: TimeFrame, candles: List[Candle]) -> List[Candle]:
        return candles

    def _save_candles(self, symbol: str, time_frame: TimeFrame, candles: List[Candle], mode: str = 'w+'):
        path = self._local_candles_path(symbol=symbol, time_frame=time_frame)
        Candle.to_csv(candles=candles, path=path, mode=mode)

    def download_candles(self, symbol: str, time_frame: TimeFrame) -> List[Candle]:
        local_candles = self._load_candles(symbol=symbol, time_frame=time_frame)

        if 0 == len(local_candles):
            symbol_info = self.market.get_symbol_info(symbol=symbol)
            start_timestamp = symbol_info.on_board_timestamp
        else:
            start_timestamp = local_candles[-1].timestamp + time_frame

        new_candles = self.market.get_candles(start_timestamp=start_timestamp, symbol=symbol, time_frame=time_frame,
                                              show_tqdm=True)

        updated_candles = local_candles + new_candles
        updated_candles = self._refine_candles(symbol=symbol, time_frame=time_frame, candles=updated_candles)
        self._save_candles(symbol=symbol, time_frame=time_frame, candles=updated_candles[:-1])

        return updated_candles

    def download_symbols_candles(self, symbols: List[str], time_frame: TimeFrame):
        for symbol in symbols:
            self.download_candles(symbol=symbol, time_frame=time_frame)
