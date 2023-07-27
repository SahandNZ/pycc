from typing import List

from pyccx.constant.symbol import Symbol
from pyccx.constant.time_frame import TimeFrame
from pyccx.exchange.bitget.future.decorators import *
from pyccx.interface.https import HttpsClient
from pyccx.interface.market import Market
from pyccx.interface.ws import WsClient
from pyccx.model.candle import Candle
from pyccx.model.symbol_info import SymbolInfo


class BitgetFutureMarket(Market):
    def __init__(self, https: HttpsClient, ws: WsClient):
        super().__init__(https, ws)

    @property
    def max_candles(self) -> int:
        pass

    def get_server_time(self) -> int:
        pass

    def get_ping(self) -> int:
        pass

    @decode_symbol
    def get_symbols_info(self) -> List[SymbolInfo]:
        endpoint = "/api/mix/v1/market/contracts"
        response = self._https.get(endpoint=endpoint)
        symbols_info = [SymbolInfo.from_bitget(item) for item in response]
        return symbols_info

    def get_candles(self, symbol: Symbol, time_frame: TimeFrame) -> List[Candle]:
        pass

    def get_historical_candles(self, symbol: Symbol, time_frame: TimeFrame, start_timestamp: int, stop_timestamp) -> \
            List[Candle]:
        pass
