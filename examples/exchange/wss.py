import argparse
import functools
import itertools
import json
import sys
import time

from pyccx.app.application import Application
from pyccx.model.candle import Candle


def print_on_message(symbol: str, time_frame: int, candle: Candle):
    print("{:<12}{:<12}{:<32}{}".format(symbol, time_frame, str(candle.datetime), candle.close))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-path', action='store', type=str, required=False, default="config.json")
    args = parser.parse_args()

    with open(args.config_path, 'r') as file:
        config_data = json.load(file)

    app = Application.from_dict(config_data['pyccx'])
    for s, tf in itertools.product(app.context.symbols, app.context.time_frames):
        on_message = functools.partial(print_on_message, s, tf)
        app.context.exchange.future.market.subscribe_candles(symbol=s, time_frame=tf, on_message=on_message)
        time.sleep(1)

    app.context.exchange.future.market.join_wss()


if __name__ == '__main__':
    sys.path.append('../..')
    main()
