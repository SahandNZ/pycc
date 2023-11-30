import json
import time
from typing import Dict, Callable, Any

from pyccx.interface.wss import WssClient


class BinanceFutureWssClient(WssClient):
    def __init__(self, key: str = None, secret_key: str = None, proxies: Dict[str, str] = None):
        super().__init__(base_url="wss://fstream.binance.com/stream", key=key, secret_key=secret_key, proxies=proxies,
                         pong_interval=5 * 60, reconnect_interval=12 * 60 * 60)
        self._stream_to_on_message: Dict[str, Callable[[Dict], Any]] = {}

    def subscribe_stream(self, stream: str, on_message: Callable[[Dict], Any]):
        stream_id = len(self._stream_to_on_message)
        payload_dict = {"method": "SUBSCRIBE", "params": [stream], "id": stream_id}
        payload = json.dumps(payload_dict)

        time.sleep(0.1)
        self._send(payload)
        self._stream_to_on_message[stream] = on_message

    def _recv(self, message_dict: Dict):
        if "stream" in message_dict:
            stream = message_dict["stream"]
            data = message_dict["data"]

            if stream in self._stream_to_on_message:
                on_message_callback = self._stream_to_on_message[stream]
                on_message_callback(data)
