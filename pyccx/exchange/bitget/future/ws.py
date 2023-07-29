from pyccx.interface.ws import WsClient


class BitgetFutureWsClient(WsClient):
    def __init__(self, key: str = None, secret_key: str = None, passphrase: str = None):
        super().__init__(base_url="", key=key, secret_key=secret_key)
        self._passphrase: str = passphrase
