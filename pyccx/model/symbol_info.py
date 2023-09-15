from typing import Dict


class SymbolInfo:
    def __init__(self):
        self.symbol: str = None
        self.base_asset: str = None
        self.quote_asset: str = None
        self.on_board_timestamp: int = None
        self.price_precision: int = None
        self.price_step: int = None
        self.volume_precision: int = None
        self.volume_step: int = None

    @staticmethod
    def from_binance(data: Dict):
        instance = SymbolInfo()

        instance.symbol = data['symbol']
        instance.base_asset = data['baseAsset']
        instance.quote_asset = data['quoteAsset']
        instance.on_board_timestamp = int(data['onboardDate']) // 1000
        instance.price_precision = int(data['pricePrecision'])
        instance.volume_precision = int(data['quantityPrecision'])

        return instance

    @staticmethod
    def from_bitget(data: Dict):
        instance = SymbolInfo()

        instance.symbol = data['symbol']
        instance.base_asset = data['baseCoin']
        instance.quote_asset = data['quoteCoin']
        instance.price_precision = int(data['pricePlace'])
        instance.price_step = int(data['priceEndStep'])
        instance.volume_precision = int(data['volumePlace'])

        return instance
