from typing import List

from src.constant.symbol import Symbol
from src.constant.time_frame import TimeFrame
from src.exchanges.bitget.future.decorators import *
from src.interface.https import HttpsClient
from src.interface.market import Market
from src.interface.ws import WsClient
from src.model.candle import Candle
from src.model.symbol_info import SymbolInfo


class BitgetFutureMarket(Market):
    def __init__(self, https: HttpsClient, ws: WsClient):
        super().__init__(https, ws)

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
