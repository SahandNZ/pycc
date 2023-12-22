import argparse
import os
import sys

from pyccx.data import load_dataframe


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--time-frame', action='store', type=int, required=False, default=300)
    parser.add_argument('--symbol', action='store', type=str, required=False, default='BTC-USDT')
    parser.add_argument('--exchange', action='store', type=str, required=False, default='binance')
    parser.add_argument('--data-root', action='store', type=str, required=False, default="./../../data")
    parser.add_argument('--base-time-frmae', action='store', type=int, required=False, default=900)
    args = parser.parse_args()

    # set env variables
    if "DATA_ROOT" not in os.environ:
        os.environ['DATA_ROOT'] = args.data_root
    if "BASE_TIME_FRAME" not in os.environ:
        os.environ['BASE_TIME_FRAME'] = args.base_time_frame

    df = load_dataframe(exchange=args.exchange, symbol=args.symbol, time_frame=args.time_frame)


if __name__ == '__main__':
    sys.path.append('..')
    main()
