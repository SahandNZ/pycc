import hashlib
import hmac
import json
from collections import OrderedDict
from datetime import datetime
from typing import Dict, Tuple
from urllib import parse
from urllib.parse import quote

from requests import Response

from pyccx.exchange.mexc.future.exception import MexcFutureHttpsException
from pyccx.interface.https import HttpsClient


class MexcFutureHttpsClient(HttpsClient):
    def __init__(self, key: str, secret_key: str):
        super().__init__(base_url="https://contract.mexc.com", key=key, secret_key=secret_key)

    def sign(self, method: str, params: Dict, request_time: int) -> str:
        if "GET" == method or "DELETE" == method:
            sign_params = parse.urlencode(OrderedDict(sorted(params.items())), quote_via=quote) if params else ""
        else:
            sign_params = json.dumps(params) if params else ""

        to_sign = f"{self._key}{request_time}{sign_params}"
        return hmac.new(self._secret_key.encode(), msg=to_sign.encode(), digestmod=hashlib.sha256).hexdigest()

    def prepare(self, method: str, params: Dict, sign: bool) -> Tuple[Dict, Dict, Dict]:
        request_time = int(datetime.now().timestamp() * 1000)
        headers = {'Content-Type': 'application/json',
                   'Request-Time': str(request_time),
                   'ApiKey': self._key,
                   'Signature': self.sign(method=method, params=params, request_time=request_time)}

        body = params if params and "POST" == method else {}
        params = params if params and ("GET" == method or "DELETE" == method) else {}
        return headers, params, body

    def parse(self, response: Response):
        if response.ok:
            response = json.loads(response.text)
            code = int(response['code'])
            if 0 == code:
                return response
            else:
                raise MexcFutureHttpsException(f"Code: {code}, Message: {response['message']}")
        else:
            raise MexcFutureHttpsException(f"Https Request Failed!")
