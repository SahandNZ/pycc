from typing import Dict

import numpy as np

from pyccx.constant.position_side import PositionSide
from pyccx.constant.position_type import PositionType


class Position:
    def __init__(self):
        self.symbol: str = None
        self.side: PositionSide = None
        self.type: PositionType = None
        self.margin: float = None
        self.volume: float = None
        self.entry_price: float = None
        self.profit: float = None
        self.leverage: int = None
        self.liquidation_price: float = None

    @staticmethod
    def from_binance(data: Dict):
        instance = Position()

        instance.symbol = data['symbol']
        instance.side = np.sign(float(data['positionAmt']))
        instance.type = data['marginType']
        instance.margin = None
        instance.volume = abs(float(data['positionAmt']))
        instance.entry_price = float(data['entryPrice'])
        instance.profit = float(data['unRealizedProfit'])
        instance.leverage = float(data['leverage'])
        instance.liquidation_price = float(data['liquidationPrice'])

        return instance

    @staticmethod
    def from_bitget(data: Dict):
        if 0 == len(data):
            return None
        elif 1 == len(data):
            data = data[0]
        else:
            data = data[0] if float(data[1]['available']) <= float(data[0]['available']) else data[1]

        instance = Position()

        instance.symbol = data['symbol']
        instance.side = data['holdSide']
        instance.type = data['marginMode']
        instance.margin = float(data['margin'])
        instance.volume = float(data['available'])
        instance.entry_price = float(data['averageOpenPrice']) if data['averageOpenPrice'] is not None else None
        instance.profit = float(data['unrealizedPL']) if data['averageOpenPrice'] is not None else None
        instance.leverage = float(data['leverage'])
        instance.liquidation_price = float(data['liquidationPrice']) if data['averageOpenPrice'] is not None else None

        return instance
