from abc import ABC

from src.interface.market import Market
from src.interface.trade import Trade


class Future(ABC):
    def __init__(self, market: Market, trade: Trade):
        self.__market = market
        self.__trade = trade

    @property
    def market(self) -> Market:
        return self.__market

    @property
    def trade(self) -> Trade:
        return self.__trade

