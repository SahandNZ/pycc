import importlib
import inspect
from typing import Dict

from pyccx.interface.future import Future
from pyccx.interface.spot import Spot
from pyccx.interface.wallet import Wallet


class Exchange:
    def __init__(self, wallet: Wallet, spot: Spot, future: Future):
        self.__wallet: Wallet = wallet
        self.__spot: Spot = spot
        self.__future: Future = future

    @staticmethod
    def __import_class(exchange: str, module_name: str, file_name: str):
        module_path = f"pyccx.exchanges.{exchange}.{module_name}.{file_name}"
        module = importlib.import_module(module_path)
        for name, cls in inspect.getmembers(module, inspect.isclass):
            if module_path == cls.__module__:
                return cls

    @staticmethod
    def __import_classes(exchange: str, module_name: str):
        https_class = Exchange.__import_class(exchange=exchange, module_name=module_name, file_name="https")
        ws_class = Exchange.__import_class(exchange=exchange, module_name=module_name, file_name="ws")
        market_class = Exchange.__import_class(exchange=exchange, module_name=module_name, file_name="market")
        trade_class = Exchange.__import_class(exchange=exchange, module_name=module_name, file_name="trade")
        return https_class, ws_class, market_class, trade_class

    @staticmethod
    def from_config(data: Dict):
        ex_name = data.pop('exchange')

        # TODO create wallet and spot instance
        wallet = None
        spot = None

        # create future instance
        https_cls, ws_cls, market_cls, trade_cls = Exchange.__import_classes(exchange=ex_name, module_name='future')
        https = https_cls(**data)
        ws = ws_cls(**data)
        future = Future(market=market_cls(https, ws), trade=trade_cls(https, ws))

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
