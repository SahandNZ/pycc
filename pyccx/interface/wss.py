import json
import ssl
import time
from abc import abstractmethod
from threading import Lock, Thread
from typing import Dict, Callable, Any, List

import websocket

from pyccx.interface.client import Client


class WssClient(Client):
    def __init__(self, base_url: str, key: str, secret_key: str, proxies: Dict[str, str], pong_interval: int,
                 reconnect_interval: int):
        super().__init__(base_url, key, secret_key, proxies)
        self._pong_interval: int = pong_interval
        self._reconnect_interval: int = reconnect_interval

        if "socks5" in proxies:
            socks5 = proxies["socks5"].split("/")[-1]
            proxy_username, others, proxy_port = socks5.split(":")
            proxy_password, proxy_host = others.split("@")
            self._proxy_params: Dict = {
                "proxy_type": "socks5",
                "http_proxy_host": proxy_host,
                "http_proxy_port": proxy_port,
                "http_proxy_auth": (proxy_username, proxy_password)}
            self.__ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        else:
            self._proxy_params: Dict = {}
            self.__ws = websocket.WebSocket()

        self._payload_history: List[str] = []

        self._recv_lock: Lock = Lock()
        self._send_lock: Lock = Lock()

        self._recv_thread: Thread = Thread(target=self._pre_recv)
        self._pong_thread: Thread = Thread(target=self._pong)
        self._reconnect_thread: Thread = Thread(target=self._reconnect)

    @abstractmethod
    def subscribe_stream(self, stream: str, on_message: Callable[[Dict], Any]):
        raise NotImplementedError()

    def join(self):
        self._recv_thread.join()

    def _ws_connect(self):
        if self.__ws.connected:
            self.__ws.close()

        self.__ws.connect(self._base_url, **self._proxy_params)

    def _connect(self):
        self._ws_connect()
        self._recv_thread.start()
        self._pong_thread.start()
        self._reconnect_thread.start()

    def _reconnect(self):
        while True:
            time.sleep(self._reconnect_interval)
            with self._send_lock:
                with self._recv_lock:
                    self._ws_connect()

            for payload in self._payload_history:
                self._send(payload)

    def _pong(self):
        while True:
            time.sleep(self._pong_interval)
            with self._send_lock:
                self.__ws.pong()

    def _pre_recv(self):
        while True:
            with self._recv_lock:
                message = self.__ws.recv()

            if 0 < len(message):
                message_dict = json.loads(message)
                self._recv(message_dict)

    @abstractmethod
    def _recv(self, message_dict: Dict):
        raise NotImplementedError()

    def _send(self, payload: str):
        if not self.__ws.connected:
            self._connect()

        if payload not in self._payload_history:
            self._payload_history.append(payload)

        with self._send_lock:
            self.__ws.send(payload)
