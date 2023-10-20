import argparse
import json
import os
import time
from datetime import datetime

from pyccx.app.application import Application
from pyccx.app.context import Context


def callback(context: Context, sleep: int):
    print("callback called at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    time.sleep(sleep)
    print("callback done   at {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data-root', action='store', type=str, required=False, default='./../data/')
    parser.add_argument('--config-path', action='store', type=str, required=False, default="config.json")
    args = parser.parse_args()

    if args.data_root is not None:
        os.environ['DATA_ROOT'] = args.data_root

    with open(args.config_path, 'r') as file:
        config_data = json.load(file)

    app = Application.from_config(config_data['pyccx'])
    app.job_queue.run_repeating(callback=callback, kwargs={"sleep": 5}, interval=10, when='open', misfire_grace_time=2)
    app.job_queue.run_repeating(callback=callback, kwargs={"sleep": 2}, interval=10, when='open', misfire_grace_time=2)
    app.run()


if __name__ == '__main__':
    main()
