from abc import abstractmethod
from typing import Dict, Callable, Any

from pyccx.interface.client import Client
from pyccx.utils.ws import Websocket


class WssClient(Client):
    def __init__(self, base_url: str, key: str, secret_key: str, proxies: Dict[str, str]):
        super().__init__(base_url, key, secret_key, proxies)
        self.__socks5 = proxies.get("socks5", None)
        self.__last_ws: Websocket = None
        self.__last_ws_streams_count: int = None

    def _send(self, payload: str):
        if self.__last_ws is None or 20 < self.__last_ws_streams_count:
            self.__last_ws: Websocket = Websocket(url=self._base_url, on_message=self._on_message, socks5=self.__socks5)
            self.__last_ws_streams_count = 0

        self.__last_ws.send(payload)
        self.__last_ws_streams_count += 1

    @abstractmethod
    def _on_message(self, message: str):
        raise NotImplementedError()

    @abstractmethod
    def subscribe_stream(self, stream: str, on_message: Callable[[Dict], Any]):
        raise NotImplementedError()

    def join(self):
        self.__last_ws.join()
