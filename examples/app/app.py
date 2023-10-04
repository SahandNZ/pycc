import argparse
import json
import os

from pyccx.app.application import Application
from pyccx.app.context import Context
from pyccx.constant.time_frame import TimeFrame


async def callback(context: Context):
    for symbol, time_frame in context.pairs:
        candles = context.live_data.get_candles(symbol, time_frame)
        print("{:<20} {:<20} {:<20} {:<20}".format(symbol, time_frame, str(candles[-3].datetime), candles[-3].close))
        print("{:<20} {:<20} {:<20} {:<20}".format(symbol, time_frame, str(candles[-2].datetime), candles[-2].close))
        print("{:<20} {:<20} {:<20} {:<20}".format(symbol, time_frame, str(candles[-1].datetime), candles[-1].close))
        print()
    print("=" * 100)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-root', action='store', type=str, required=False, default='./../data/')
    parser.add_argument('--symbol', action='store', type=str, required=False, default='BTC-USDT')
    parser.add_argument('--time-frame', action='store', type=int, required=False, default=TimeFrame.HOUR1)
    parser.add_argument('--config-path', action='store', type=str, required=False, default="config.json")
    args = parser.parse_args()

    if args.data_root is not None:
        os.environ['DATA_ROOT'] = args.data_root

    with open(args.config_path, 'r') as file:
        config_data = json.load(file)

    app = Application.from_config(config_data['pyccx'])
    app.job_queue.run_once(callback=callback)
    app.job_queue.run_repeating(callback=callback, interval=60, when='open', misfire_grace_time=30)
    app.run()


if __name__ == '__main__':
    main()
