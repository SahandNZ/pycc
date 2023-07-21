from datetime import datetime
from typing import Dict

from pyccx.constant.order_side import OrderSide
from pyccx.constant.order_status import OrderStatus
from pyccx.constant.order_type import OrderType


class Order:
    def __init__(self):
        self.id: str = None
        self.symbol: str = None
        self.timestamp: int = None
        self.datetime: datetime = None
        self.type: OrderType = None
        self.status: OrderStatus = None
        self.side: OrderSide = None
        self.volume: float = None
        self.price: float = None

    @staticmethod
    def from_bitget(data: Dict):
        instance = Order()

        instance.id = data['orderId']
        instance.symbol = data['symbol']
        instance.datetime = datetime.fromtimestamp(int(data['cTime']) / 1000)
        instance.timestamp = int(int(data['cTime']) / 1000)
        instance.type = data['orderType']
        instance.status = data['state']
        instance.side = data['side']
        instance.volume = float(data['size'])
        instance.price = float(data['price'])

        return instance

    @staticmethod
    def from_mex(data: Dict):
        instance = Order()

        instance.id = str(data['orderId'])
        instance.symbol = int(data['symbol'])
        instance.timestamp = instance.datetime.timestamp()
        instance.datetime = datetime.strptime(data['createTime'], "")
        instance.type = int(data['orderType'])
        instance.status = int(data['state'])
        instance.side = int(data['side'])
        instance.volume = float(data['volume'])
        instance.price = float(data['price'])

        return instance
