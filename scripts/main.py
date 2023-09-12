import argparse
import json
import sys
from typing import List

from examples.future import future_examples
from examples.spot import spot_examples
from examples.wallet import wallet_examples
from pyccx.constant.time_frame import TimeFrame
from pyccx.data_collector import DataCollector
from pyccx.interface.exchange import Exchange


def run_examples(exchange: Exchange, symbol: str, time_frame: TimeFrame):
    print("Exchange examples")
    wallet_examples(exchange)
    spot_examples(exchange, symbol, time_frame)
    future_examples(exchange, symbol, time_frame)


def download_candles(exchange: Exchange, symbols: List[str]):
    data_collector = DataCollector(exchange=exchange, market=exchange.future.market, data_root='./../data')
    data_collector.download_symbols_candles(symbols=symbols, time_frame=TimeFrame.MIN1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--run-examples', action='store_true')
    parser.add_argument('-d', '--download-candles', action='store_true')
    parser.add_argument('-tf', '--time-frame', action='store', type=int, required=False, default=60)
    parser.add_argument('-s', '--symbol', action='store', type=str, required=False, default='BTC-USDT')
    parser.add_argument('-c', '--config-path', action='store', type=str, required=False, default="config.json")
    args = parser.parse_args()

    with open(args.config_path, 'r') as file:
        config_data = json.load(file)
    exchange = Exchange.from_config(config_data['exchange'])

    if args.run_examples:
        run_examples(exchange=exchange, symbol=args.symbol, time_frame=args.time_frame)
    if args.download_candles:
        download_candles(exchange=exchange, symbols=config_data['symbols'])


if __name__ == '__main__':
    sys.path.append('..')
    main()
