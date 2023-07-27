from datetime import datetime
from typing import List

from pyccx.constant.time_frame import TimeFrame
from pyccx.exchange.bitget.future.decorator import *
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
        return 200

    def get_server_time(self) -> int:
        pass

    def get_ping(self) -> int:
        pass

    @symbol_decorator
    def get_symbols_info(self) -> List[SymbolInfo]:
        endpoint = "/api/mix/v1/market/contracts"
        response = self._https.get(endpoint=endpoint)
        symbols_info = [SymbolInfo.from_bitget(item) for item in response]
        return symbols_info

    @symbol_decorator
    def get_candles(self, symbol: str, time_frame: TimeFrame) -> List[Candle]:
        endpoint = "/api/mix/v1/market/history-candles"
        stop_timestamp = datetime.now().timestamp() // time_frame * time_frame
        start_timestamp = stop_timestamp - self.max_candles * time_frame
        params = {'symbol': symbol,
                  'granularity': time_frame_encoder(time_frame),
                  'startTime': str(int(start_timestamp * 1000)),
                  'endTime': str(int(stop_timestamp * 1000))}
        response = self._https.get(endpoint=endpoint, params=params)
        candles = [Candle.from_bitget(item) for item in response]
        return candles

    @symbol_decorator
    def get_historical_candles(self, symbol: str, time_frame: TimeFrame, start_timestamp: int, stop_timestamp) -> \
            List[Candle]:
        endpoint = "/api/mix/v1/market/history-candles"
        limit = (stop_timestamp - start_timestamp) // time_frame
        params = {'symbol': symbol,
                  'granularity': time_frame_encoder(time_frame),
                  'startTime': str(int(start_timestamp * 1000)),
                  'endTime': str(int(stop_timestamp * 1000)),
                  'limit': str(int(limit))}
        response = self._https.get(endpoint=endpoint, params=params)
        candles = [Candle.from_bitget(item) for item in response]
        return candles
