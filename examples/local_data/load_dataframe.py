import argparse
import os
import sys

from pyccx.data.local_data import load_dataframe


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--time-frame', action='store', type=int, required=False, default=300)
    parser.add_argument('--symbol', action='store', type=str, required=False, default='BTC-USDT')
    parser.add_argument('--exchange', action='store', type=str, required=False, default='binance')
    parser.add_argument('--data-root', action='store', type=str, required=False, default="./../data")
    args = parser.parse_args()

    if args.data_root is not None:
        os.environ['DATA_ROOT'] = args.data_root

    df = load_dataframe(exchange=args.exchange, symbol=args.symbol, time_frame=args.time_frame)


if __name__ == '__main__':
    sys.path.append('..')
    main()
