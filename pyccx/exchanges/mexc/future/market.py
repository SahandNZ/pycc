from datetime import datetime
from typing import List

from pyccx.constant.symbol import Symbol
from pyccx.constant.time_frame import TimeFrame
from pyccx.interface.https import HttpsClient
from pyccx.interface.market import Market
from pyccx.interface.ws import WsClient
from pyccx.model.candle import Candle
from pyccx.model.symbol_info import SymbolInfo


class MexcFutureMarket(Market):
    def __init__(self, https: HttpsClient, ws: WsClient):
        super().__init__(https, ws)

    def get_server_time(self) -> int:
        endpoint = "api/v1/contract/ping"
        response = self._https.get(endpoint=endpoint)
        server_time = int(response['data'])
        return server_time

    def get_ping(self) -> int:
        local_timestamp = int(datetime.now().timestamp() * 1000)
        server_timestamp = self.get_server_time()
        ping = int(server_timestamp - local_timestamp)
        return ping

    def get_symbols_info(self) -> List[SymbolInfo]:
        endpoint = "api/v1/contract/detail"
        response = self._https.get(endpoint=endpoint)
        return response

    def get_candles(self, symbol: Symbol, time_frame: TimeFrame) -> List[Candle]:
        pass
