import asyncio
import copy
from typing import Dict, List

from pyccx.app.context import Context
from pyccx.app.job_queue import JobQueue
from pyccx.constant.time_frame import TimeFrame
from pyccx.interface.exchange import Exchange
from pyccx.utils import call_with_dict


class Application:
    def __init__(self, exchange: Exchange, symbols: List[str], time_frames: List[TimeFrame], candles_count: int = None,
                 delay: int = 0.1):
        self.__context = Context(exchange=exchange, symbols=symbols, time_frames=time_frames,
                                 candles_count=candles_count)
        self.__job_queue = JobQueue(context=self.context, delay=delay)

    @staticmethod
    def from_config(config_dict: Dict):
        exchange = Exchange.from_config(config_dict)

        dct = copy.deepcopy(config_dict)
        dct['exchange'] = exchange
        app = call_with_dict(Application, dct)

        return app

    @property
    def context(self) -> Context:
        return self.__context

    @property
    def job_queue(self) -> JobQueue:
        return self.__job_queue

    def run(self):
        self.job_queue.start()
        asyncio.get_event_loop().run_forever()
