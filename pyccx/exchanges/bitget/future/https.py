import base64
import hashlib
import hmac
import json
from datetime import datetime
from typing import Dict, Tuple
from urllib import parse

from requests import Response

from pyccx.exchanges.bitget.future.exception import BitgetFutureHttpsException
from pyccx.interface.https import HttpsClient


class BitgetFutureHttpsClient(HttpsClient):
    def __init__(self, passphrase: str, key: str, secret_key: str):
        super().__init__(base_url="https://api.bitget.com", key=key, secret_key=secret_key)
        self._passphrase: str = passphrase

    def sign(self, method: str, endpoint: str, params: Dict, request_time: int) -> str:
        params_str = '?' + parse.urlencode(list(params.items())) if "GET" == method and params is not None else ""
        body_str = json.dumps(params) if "POST" == method else ""
        to_sign = str(request_time) + method.upper() + endpoint + params_str + body_str
        payload = hmac.new(self._secret_key.encode('utf-8'), to_sign.encode('utf-8'), hashlib.sha256).digest()
        return base64.b64encode(payload).decode('utf-8')

    def prepare(self, method: str, endpoint: str, params: Dict, sign: bool) -> Tuple[Dict, Dict, Dict]:
        request_time = int(datetime.now().timestamp() * 1000)
        headers = {
            'ACCESS-KEY': self._key,
            'ACCESS-SIGN': self.sign(method, endpoint, params, request_time),
            'ACCESS-TIMESTAMP': str(request_time),
            'ACCESS-PASSPHRASE': self._passphrase,
            'Content-Type': 'application/json',
        }

        body = json.dumps(params) if "POST" == method else ""
        params = params if "GET" == method and params is not None else {}

        return headers, params, {"data": body}

    def parse(self, response: Response):
        response_map = json.loads(response.text)
        code = int(response_map['code'])
        message = response_map['msg']
        if 0 == code:
            return response_map['data']
        else:
            raise BitgetFutureHttpsException(f"Code: {code}, Message: {message}")
