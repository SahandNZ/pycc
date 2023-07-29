from pyccx.interface.ws import WsClient


class BinanceFutureWsClient(WsClient):
    def __init__(self, key: str = None, secret_key: str = None):
        super().__init__(base_url="", key=key, secret_key=secret_key)
