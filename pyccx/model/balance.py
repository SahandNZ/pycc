from typing import Dict


class Balance:
    def __init__(self):
        self.asset: str = None
        self.total: float = None
        self.available: float = None
        self.frozen: float = None

    @staticmethod
    def from_binance(data: Dict):
        instance = Balance()

        instance.asset = data['asset']
        instance.total = round(float(data['balance']), 2)
        instance.available = round(float(data['availableBalance']), 2)

        return instance

    @staticmethod
    def from_bitget(data: Dict):
        instance = Balance()

        instance.asset = data['marginCoin']
        instance.available = round(float(data['available']), 2)
        instance.frozen = round(float(data['locked']), 2)

        return instance

    @staticmethod
    def from_mexc(data: Dict):
        instance = Balance()

        instance.asset = data['currency']
        instance.available = round(float(data['availableBalance']), 2)
        instance.frozen = round(float(data['frozenBalance']), 2)
        instance.margin = round(float(data['positionMargin']), 2)

        return instance
