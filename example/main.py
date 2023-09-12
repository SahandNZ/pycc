import argparse
import json
import sys

from pyccx.interface.exchange import Exchange


def main():
    sys.path.append('..')

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config-path', action='store', type=str, required=False, default="config.json")
    parser.add_argument('-e', '--exchange', action='store', type=str, required=False, default="binance")
    parser.add_argument('-s', '--symbol', action='store', type=str, required=False, default='BTC-USDT')
    args = parser.parse_args()

    with open(args.config_path, 'r') as file:
        data = json.load(file)

    data = data[args.exchange]
    exchange = Exchange.from_config(data)

    # get balance
    balance = exchange.future.trade.get_balance()
    print("\t\t- Get balance")
    print("\t\t\t- {:<32} {}".format("Total", balance.total))
    print("\t\t\t- {:<32} {}".format("Available", balance.available))

    # cancel all open orders
    print("\t\t- Cancel all open orders")
    exchange.future.trade.cancel_all_orders(symbol=args.symbol)

    # get open orders
    orders = exchange.future.trade.get_open_orders(symbol=args.symbol)
    print("\t\t- Get open orders")
    print("\t\t\t- {:<32} {}".format("orders count", len(orders)))

    # get position
    position = exchange.future.trade.get_open_position(symbol=args.symbol)
    print("\t\t- Get position")
    print("\t\t\t- {:<32} {}".format("symbol", position.symbol))
    print("\t\t\t- {:<32} {}".format("side", position.side))
    print("\t\t\t- {:<32} {}".format("volume", position.volume))
    print("\t\t\t- {:<32} {}".format("Leverage", position.leverage))
    print("\t\t\t- {:<32} {}".format("Entry price", position.entry_price))
    print("\t\t\t- {:<32} {}".format("Liquidation price", position.liquidation_price))


if __name__ == '__main__':
    main()
