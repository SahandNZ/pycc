from abc import ABC, abstractmethod
from typing import Dict, Tuple
from urllib import parse

import requests as requests
from requests import Response


class HttpsClient(ABC):
    def __init__(self, base_url: str, key: str, secret_key: str):
        self._base_url: str = base_url
        self._key: str = key
        self._secret_key: str = secret_key

    @abstractmethod
    def sign(self, method: str, endpoint: str, params: Dict, timestamp: int) -> str:
        raise NotImplementedError()

    @abstractmethod
    def prepare(self, method: str, endpoint: str, params: Dict, sign: bool) -> Tuple[Dict, Dict, Dict]:
        raise NotImplementedError()

    @abstractmethod
    def parse(self, response: Response):
        raise NotImplementedError()

    def __request(self, method: str, endpoint: str, params: Dict, sign: bool):
        url = parse.urljoin(self._base_url, endpoint)
        headers, params, body = self.prepare(method, endpoint, params, sign)
        response = requests.request(method=method, url=url, headers=headers, params=params, **body)
        data = self.parse(response)
        return data

    def get(self, endpoint: str, params: Dict = None, sign: bool = False):
        return self.__request(method='GET', endpoint=endpoint, params=params, sign=sign)

    def post(self, endpoint: str, params: Dict = None, sign: bool = False):
        return self.__request(method='POST', endpoint=endpoint, params=params, sign=sign)

    def delete(self, endpoint: str, params: Dict = None, sign: bool = False):
        return self.__request(method='DELETE', endpoint=endpoint, params=params, sign=sign)
