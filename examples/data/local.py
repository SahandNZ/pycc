import argparse
import sys

from pyccx.data import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--symbol', action='store', type=str, required=False, default='BTC-USDT')
    parser.add_argument('--time-frame', action='store', type=int, required=False, default=300)
    args = parser.parse_args()

    symbols = get_local_symbols()
    df = load_dataframe(symbol=args.symbol, time_frame=args.time_frame)


if __name__ == '__main__':
    sys.path.append('..')
    main()
