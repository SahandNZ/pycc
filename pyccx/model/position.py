from typing import Dict

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
    def from_bitget(data: Dict):
        if 0 == len(data):
            instance = Position()
            instance.volume = 0
            return instance
        elif 1 == len(data):
            data = data[0]
        else:
            long_volume = float(data[0]['available'])
            short_volume = float(data[1]['available'])
            data = data[0] if short_volume <= long_volume else data[1]

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
