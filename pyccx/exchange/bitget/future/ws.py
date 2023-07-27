from pyccx.interface.ws import WsClient


class BitgetFutureWsClient(WsClient):
    def __init__(self, passphrase: str, key: str, secret_key: str):
        super().__init__(base_url="", key=key, secret_key=secret_key)
        self._passphrase: str = passphrase
