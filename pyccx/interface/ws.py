from abc import ABC


class WsClient(ABC):
    def __init__(self, base_url: str, key: str, secret_key: str):
        self._base_url: str = base_url
        self._key: str = key
        self._secret_key: str = secret_key
