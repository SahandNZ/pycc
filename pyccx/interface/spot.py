from abc import ABC, abstractmethod

from pyccx.interface.market import Market
from pyccx.interface.trade import Trade


class Spot(ABC):
    @property
    @abstractmethod
    def trade(self) -> Trade:
        pass

    @property
    @abstractmethod
    def market(self) -> Market:
        pass
