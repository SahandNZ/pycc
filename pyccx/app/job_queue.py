from datetime import datetime
from typing import Callable, List

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyccx.app.context import Context
from pyccx.app.job import Job


class JobQueue:
    def __init__(self, context: Context, delay: int):
        self.__context: Context = context
        self.__delay: int = delay
        self.__scheduler = AsyncIOScheduler()

    @property
    def context(self) -> Context:
        return self.__context

    @property
    def delay(self) -> int:
        return self.__delay

    @property
    def scheduler(self) -> AsyncIOScheduler:
        return self.__scheduler

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()

    def _cast_args(self, args: List) -> List:
        if args is None:
            return []
        else:
            return list(args)

    def _cast_when(self, interval: int, when: str) -> datetime:
        if 'any' == when:
            return None
        elif 'open' == when:
            next_timestamp = datetime.now().timestamp() // interval * interval + interval + self.delay
            return datetime.fromtimestamp(next_timestamp)

    def run_once(self, callback: Callable, args: List = None) -> Job:
        args = self._cast_args(args)

        job = Job(callback=callback)
        job.aps_job = self.scheduler.add_job(
            func=job.run,
            name=job.name,
            args=(self.__context, args),
        )

        return job

    def run_repeating(self, callback: Callable, interval: int, args: List = None, when: str = 'any') -> Job:
        args = self._cast_args(args)
        start_date = self._cast_when(interval=interval, when=when)

        job = Job(callback=callback)
        job.aps_job = self.scheduler.add_job(
            func=job.run,
            name=job.name,
            trigger="interval",
            args=(self.__context, args),
            start_date=start_date,
            seconds=interval,
        )

        return job
