import abc
import asyncio
import datetime
import time


class Clock(abc.ABC):
    @abc.abstractmethod
    def now(self) -> int:
        """Return current timestamp in ms"""

    @abc.abstractmethod
    def sleep(self, seconds: float):
        """Syncronous sleep for several seconds"""

    @abc.abstractmethod
    async def asleep(self, seconds: float):
        """Asyncronous sleep for several seconds"""

    @abc.abstractmethod
    def timestamp(self) -> int:
        """Return current timestamp in ms"""


class UtcClock(Clock):
    def now(self) -> int:
        return int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)

    def sleep(self, seconds: float):
        time.sleep(seconds)

    async def asleep(self, seconds: float):
        await asyncio.sleep(seconds)

    def timestamp(self) -> int:
        return int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
