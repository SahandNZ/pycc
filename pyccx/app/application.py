import asyncio
from typing import Dict

from pyccx.app.context import Context
from pyccx.app.job_queue import JobQueue
from pyccx.constant.time_frame import TimeFrame
from pyccx.interface.exchange import Exchange
from pyccx.utils import call_with_dict


class Application:
    def __init__(self, exchange: Exchange, symbol: str, time_frame: TimeFrame, delay: int = 0.1):
        self.__context = Context(exchange=exchange, symbol=symbol, time_frame=time_frame)
        self.__job_queue = JobQueue(context=self.context, delay=delay)

    @staticmethod
    def from_config(config_dict: Dict):
        exchange = Exchange.from_config(config_dict)

        dct = {'exchange': exchange, 'symbol': config_dict['symbol'], 'time_frame': config_dict['time-frame']}
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
