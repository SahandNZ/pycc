from abc import ABC, abstractmethod

from src.interface.market import Market
from src.interface.trade import Trade


class Spot(ABC):
    @property
    @abstractmethod
    def trade(self) -> Trade:
        pass

    @property
    @abstractmethod
    def market(self) -> Market:
        pass
