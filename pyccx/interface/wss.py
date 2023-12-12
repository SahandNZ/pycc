from abc import abstractmethod
from typing import Dict, Callable, Any

from pyccx.interface.client import Client
from pyccx.utils.ws import Websocket


class WssClient(Client):
    def __init__(self, base_url: str, key: str, secret_key: str, proxies: Dict[str, str]):
        super().__init__(base_url, key, secret_key, proxies)
        self.__ws: Websocket = Websocket(url=base_url, on_message=self._on_message, socks5=proxies.get("socks5", None))

    def _send(self, payload: str):
        self.__ws.send(payload)

    @abstractmethod
    def _on_message(self, message: str):
        raise NotImplementedError()

    @abstractmethod
    def subscribe_stream(self, stream: str, on_message: Callable[[Dict], Any]):
        raise NotImplementedError()

    def join(self):
        self.__ws.join()
