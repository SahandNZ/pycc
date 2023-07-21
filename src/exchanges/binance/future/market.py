from datetime import datetime
from typing import List

from src.constant.symbol import Symbol
from src.constant.time_frame import TimeFrame
from src.exchanges.binance.future.decorators import encode_symbol, encode_time_frame
from src.interface.https import HttpsClient
from src.interface.market import Market
from src.interface.ws import WsClient
from src.model.candle import Candle
from src.model.symbol_info import SymbolInfo


class BinanceFutureMarket(Market):
    def __init__(self, https: HttpsClient, ws: WsClient):
        super().__init__(https, ws)

    def max_candles(self) -> int:
        return 1500

    def get_server_time(self) -> int:
        endpoint = '/fapi/v1/time'
        response = self._https.get(endpoint=endpoint)
        server_time = int(response['serverTime'])
        return server_time

    def get_ping(self) -> int:
        local = datetime.now().timestamp() * 1000
        server = self.get_server_time()
        ping = round(server - local)
        return ping

    def get_symbols_info(self) -> List[SymbolInfo]:
        endpoint = '/fapi/v1/exchangeInfo'
        response = self._https.get(endpoint=endpoint)
        perpetuals = [item for item in response['symbols'] if 'PERPETUAL' == item['contractType']]
        symbols_info = [SymbolInfo.from_binance(item) for item in perpetuals]
        return symbols_info

    @encode_symbol
    @encode_time_frame
    def get_candles(self, symbol: Symbol, time_frame: TimeFrame) -> List[Candle]:
        endpoint = '/fapi/v1/klines'
        params = {'symbol': symbol, 'interval': time_frame}
        response = self._https.get(endpoint=endpoint, params=params)
        candles = [Candle.from_binance(item) for item in response]
        return candles

    @encode_symbol
    @encode_time_frame
    def get_historical_candles(self, symbol: Symbol, time_frame: TimeFrame, start_timestamp: int, stop_timestamp) -> \
            List[Candle]:
        endpoint = '/fapi/v1/klines'
        limit = (stop_timestamp - start_timestamp) // time_frame
        params = {'symbol': symbol, 'interval': time_frame, 'startTime': start_timestamp * 1000,
                  'endTime': stop_timestamp * 1000, 'limit': limit}
        response = self._https.get(endpoint=endpoint, params=params)
        candles = [Candle.from_binance(item) for item in response]
        return candles
