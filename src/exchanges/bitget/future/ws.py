from src.interface.ws import WsClient


class BitgetFutureWsClient(WsClient):
    def __init__(self, pass_phrase: str, key: str, secret_key: str):
        super().__init__(base_url="", key=key, secret_key=secret_key)
        self._pass_phrase: str = pass_phrase
