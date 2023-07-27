from typing import Dict

from pyccx.interface.future import Future
from pyccx.interface.spot import Spot
from pyccx.interface.wallet import Wallet
from pyccx.utils.utils import import_class


class Exchange:
    def __init__(self, wallet: Wallet, spot: Spot, future: Future):
        self.__wallet: Wallet = wallet
        self.__spot: Spot = spot
        self.__future: Future = future

    @staticmethod
    def from_config(conf_dict: Dict):
        exchange = conf_dict.pop('exchange')

        # TODO create wallet and spot instance
        wallet = None
        spot = None

        # create future instance
        https_cls = import_class(module=f"pyccx.exchange.{exchange}.future.https")
        ws_cls = import_class(module=f"pyccx.exchange.{exchange}.future.ws")
        market_cls = import_class(module=f"pyccx.exchange.{exchange}.future.market")
        trade_cls = import_class(module=f"pyccx.exchange.{exchange}.future.trade")

        https = https_cls(**conf_dict)
        ws = ws_cls(**conf_dict)
        market = market_cls(https, ws)
        trade = trade_cls(https, ws)
        future = Future(market=market, trade=trade)

        return Exchange(wallet=wallet, spot=spot, future=future)

    @property
    def wallet(self) -> Wallet:
        return self.__wallet

    @property
    def spot(self) -> Spot:
        return self.__spot

    @property
    def future(self) -> Future:
        return self.__future
