import argparse
import json
import logging
import sys

from example.future import future_examples
from example.spot import spot_examples
from example.wallet import wallet_examples
from pyccx.constant.time_frame import TimeFrame
from pyccx.interface.exchange import Exchange


def exchange_examples(exchange: Exchange, symbol: str, time_frame: TimeFrame):
    print("Exchange examples")
    wallet_examples(exchange)
    spot_examples(exchange, symbol, time_frame)
    future_examples(exchange, symbol, time_frame)


def main():
    sys.path.append('..')

    logging.basicConfig(format='[%(asctime)s] %(name)s | %(levelname)s | %(message)s', level=logging.INFO,
                        datefmt='%Y-%m-%d %H:%M:%S')

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-path', action='store', type=str, required=False, default="config.json")
    parser.add_argument('-e', '--exchange', action='store', type=str, required=False, default="bitget")
    parser.add_argument('-s', '--symbol', action='store', type=str, required=False, default='XLM-USDT')
    parser.add_argument('-tf', '--time-frame', action='store', type=int, required=False, default=60)
    args = parser.parse_args()

    with open(args.config_path, 'r') as file:
        data = json.load(file)

    data = data[args.exchange]
    exchange = Exchange.from_config(data)
    exchange_examples(exchange, args.symbol, args.time_frame)


if __name__ == '__main__':
    main()
