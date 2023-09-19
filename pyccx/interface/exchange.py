from pyccx.interface.future import Future
from pyccx.interface.spot import Spot
from pyccx.interface.wallet import Wallet
from pyccx.utils import import_class, call_with_dict
from typing import Dict


class Exchange:
    def __init__(self, exchange: str, api_key: str = None, secret_key: str = None, passphrase: str = None):
        self.__exchange: str = exchange

        # import classes
        https_cls = import_class(module=f"pyccx.exchange.{exchange}.future.https")
        ws_cls = import_class(module=f"pyccx.exchange.{exchange}.future.ws")
        market_cls = import_class(module=f"pyccx.exchange.{exchange}.future.market")
        trade_cls = import_class(module=f"pyccx.exchange.{exchange}.future.trade")

        # create protocol instances
        params = {"api_key": api_key, "secret_key": secret_key, "passphrase": passphrase}
        https = call_with_dict(https_cls, params)
        ws = call_with_dict(ws_cls, params)

        # TODO create wallet and spot instances
        self.__wallet: Wallet = None
        self.__spot: Spot = None

        # create future instance
        future_market = market_cls(https, ws)
        future_trade = trade_cls(https, ws)
        self.__future: Future = Future(market=future_market, trade=future_trade)

    @staticmethod
    def from_config(config_dict: Dict):
        return call_with_dict(Exchange, config_dict)

    @property
    def exchange(self) -> str:
        return self.__exchange

    @property
    def wallet(self) -> Wallet:
        return self.__wallet

    @property
    def spot(self) -> Spot:
        return self.__spot

    @property
    def future(self) -> Future:
        return self.__future
