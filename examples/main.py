import argparse
import json
import os
import sys
from typing import List

from examples.future import future_examples
from examples.spot import spot_examples
from examples.wallet import wallet_examples
from pyccx.constant.time_frame import TimeFrame
from pyccx.data.local_data import LocalData
from pyccx.interface.exchange import Exchange


def print_ping(exchange: Exchange):
    ping = exchange.future.market.get_ping()
    print("\t\t- {:<40} {}ms".format("Ping to {}".format(exchange.name), ping))


def run_examples(exchange: Exchange, symbol: str, time_frame: TimeFrame):
    print("Exchange examples")
    wallet_examples(exchange)
    spot_examples(exchange, symbol, time_frame)
    future_examples(exchange, symbol, time_frame)


def download_candles(exchange: Exchange, symbols: List[str], time_frame: TimeFrame):
    local_data = LocalData(exchange=exchange)
    local_data.download_symbols_candles(symbols=symbols, time_frame=time_frame)


def close_position(exchange: Exchange, symbol: str):
    # get position to close position
    position = exchange.future.trade.get_open_position(symbol=symbol)
    print("\t\t- Get position")
    print("\t\t\t- {:<32} {}".format("symbol", position.symbol))
    print("\t\t\t- {:<32} {}".format("side", position.side))
    print("\t\t\t- {:<32} {}".format("volume", position.volume))
    print("\t\t\t- {:<32} {}".format("Leverage", position.leverage))
    print("\t\t\t- {:<32} {}".format("Entry price", position.entry_price))
    print("\t\t\t- {:<32} {}".format("Liquidation price", position.liquidation_price))

    # post market order to close current position
    reverse_side = -1 * position.side
    order_id = exchange.future.trade.set_market_order(symbol=symbol, side=reverse_side, volume=position.volume)
    print("\t\t- Post Market order")
    print("\t\t\t- {:<32} {}".format("Buy market order", order_id))

    # get position to check is position closed
    position = exchange.future.trade.get_open_position(symbol=symbol)
    print("\t\t- Get position")
    print("\t\t\t- {:<32} {}".format("symbol", position.symbol))
    print("\t\t\t- {:<32} {}".format("side", position.side))
    print("\t\t\t- {:<32} {}".format("volume", position.volume))
    print("\t\t\t- {:<32} {}".format("Leverage", position.leverage))
    print("\t\t\t- {:<32} {}".format("Entry price", position.entry_price))
    print("\t\t\t- {:<32} {}".format("Liquidation price", position.liquidation_price))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--print-ping', action='store_true')
    parser.add_argument('--run-examples', action='store_true')
    parser.add_argument('--download-candles', action='store_true')
    parser.add_argument('--close-positions', action='store_true')
    parser.add_argument('--data-root', action='store', type=str, required=False)
    parser.add_argument('--time-frame', action='store', type=int, required=False, default=60)
    parser.add_argument('--symbol', action='store', type=str, required=False, default='BTC-USDT')
    parser.add_argument('--config-path', action='store', type=str, required=False, default="config.json")
    args = parser.parse_args()

    if args.data_root is not None:
        os.environ['DATA_ROOT'] = args.data_root

    with open(args.config_path, 'r') as file:
        config_data = json.load(file)
    exchange = Exchange.from_config(config_data['exchange'])

    if args.print_ping:
        print_ping(exchange)
    if args.run_examples:
        run_examples(exchange=exchange, symbol=args.symbol, time_frame=args.time_frame)
    if args.download_candles:
        symbols = config_data['symbols']
        download_candles(exchange=exchange, symbols=symbols, time_frame=args.time_frame)
    if args.close_positions:
        close_position(exchange=exchange, symbol=args.symbol)


if __name__ == '__main__':
    sys.path.append('..')
    main()
