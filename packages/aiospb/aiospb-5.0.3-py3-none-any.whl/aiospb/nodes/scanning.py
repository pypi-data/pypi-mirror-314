import abc
import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any, Self

from .. import Clock, UtcClock
from ..data import DataType, Metric, PropertySet, PropertyValue, Quality, ValueType

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class MetricCore:
    """Metric data, stable for a session"""

    name: str
    datatype: DataType
    properties: PropertySet = field(default_factory=PropertySet)
    alias: int = 0
    is_transient: bool = False

    def create_metric(
        self, value: ValueType, timestamp: int, quality: Quality | None = None
    ) -> Metric:
        """Create metric from the metric core"""
        props = self.properties
        if quality is not None:
            props_data = self.properties.as_dict()
            props_data["quality"] = {"value": quality.value, "dataType": "Int32"}
            props = PropertySet.from_dict(props_data)

        return Metric(
            timestamp,
            value,
            self.datatype,
            self.alias,
            self.name,
            props,
            self.is_transient,
        )

    # @classmethod
    # def from_dict(cls, dump: dict[str, Any]) -> Self:
    #     datatype = (
    #         DataType(dump["dataType"])
    #         if type(dump["dataType"]) is int
    #         else DataType[dump["dataType"]]
    #     )
    #     properties = (
    #         PropertySet.from_dict(dump["properties"])
    #         if "properties" in dump
    #         else PropertySet()
    #     )
    #     return cls(
    #         dump["name"],
    #         datatype,
    #         properties,
    #         dump.get("alias", 0),
    #         dump.get("is_transient", False),
    #     )


class MetricsNet(abc.ABC):
    # @abc.abstractmethod
    # async def smap(self) -> dict[str, int]:
    #     """List all name of metrics available and their aliases, 0 it does not have"""

    @abc.abstractmethod
    async def get_metric_cores(self, filter: str = "") -> list[MetricCore]:
        """List available metrics in the net with all its properties"""

    @abc.abstractmethod
    async def read_value(self, metric_name: str = "", alias: int = 0) -> ValueType:
        """Read a value to a metric"""

    @abc.abstractmethod
    async def write_value(
        self, value: ValueType, metric_name: str = "", alias: int = 0
    ):
        """Write a value to a metric"""


@dataclass
class _Sample:
    timestamp: int
    value: ValueType
    quality: Quality

    @classmethod
    async def read(
        cls,
        metrics_net: MetricsNet,
        clock: Clock,
        metric_name: str = "",
        alias: int = 0,
    ) -> Self:
        if not alias and not metric_name:
            raise ValueError("Metric Name and alias can not be null at the same time")
        try:
            value = await metrics_net.read_value(metric_name)
            return cls(clock.timestamp(), value, Quality.GOOD)
        except asyncio.CancelledError:
            return cls(clock.timestamp(), None, Quality.STALE)
        except Exception as e:
            logger.error(f"Exception when reading metric {metric_name}:{alias}")
            logger.exception(e)
            return cls(clock.timestamp(), None, Quality.BAD)


@dataclass
class _Scan:
    scan_rate: int
    datatype: DataType
    quality: Quality
    value: ValueType = None
    alias: int = 0
    name: str = ""

    def update(self, sample: _Sample) -> Metric | None:
        if sample.quality == self.quality and sample.value == self.value:
            return

        if self.quality != Quality.GOOD and sample.quality == self.quality:
            return

        props = (
            PropertySet()
            if self.quality == sample.quality
            else PropertySet(
                ("quality",), (PropertyValue(sample.quality.value, DataType.Int32),)
            )
        )
        self.quality = sample.quality

        value = sample.value if sample.quality == Quality.GOOD else self.value
        self.value = value

        name = "" if self.alias else self.name
        return Metric(sample.timestamp, value, self.datatype, self.alias, name, props)

    def plan_next_scan(self, schedules: dict[int, list[Self]], clock: Clock):
        timestamp = ((clock.timestamp() // self.scan_rate) + 1) * self.scan_rate
        if timestamp not in schedules:
            schedules[timestamp] = []

        schedules[timestamp].append(self)


class Scanner:
    def __init__(
        self,
        metrics_net: MetricsNet,
        scan_rate: int = 60000,
        clock: Clock | None = None,
    ):
        self._net = metrics_net
        self._clock = clock or UtcClock()
        self._scan_rate = scan_rate

        self._queue = asyncio.Queue()
        self._schedules = {}  # scans ordered by timestamp to be triggered
        self._tasks = {}  # scannings to be done in the future

    @property
    def scan_rate(self) -> float:
        return self._scan_rate

    async def deliver_changes(self, timeout: float = 0.0) -> list[Metric]:
        """Return last changes"""
        if timeout:
            return await asyncio.wait_for(self._queue.get(), timeout=timeout)
        return await self._queue.get()

    async def _read_births(self) -> list[Metric]:
        cores = await self._net.get_metric_cores()

        readings = [
            asyncio.create_task(_Sample.read(self._net, self._clock, core.name))
            for core in cores
        ]
        _, pending = await asyncio.wait(readings, timeout=self._scan_rate / 1000)
        for reading in pending:
            reading.cancel()
        await asyncio.gather(*pending, return_exceptions=True)

        births = []
        for core, reading in zip(cores, readings):
            sample = reading.result()
            births.append(
                core.create_metric(sample.value, sample.timestamp, sample.quality)
            )

        return births

    async def start(self) -> list[Metric]:
        ts = self._clock.timestamp()
        node_controls = [
            Metric(ts, False, DataType.Boolean, name="Node Control/Reboot"),
            Metric(ts, False, DataType.Boolean, name="Node Control/Rebirth"),
            Metric(
                ts,
                int(self._scan_rate * 1000),
                DataType.Int64,
                name="Node Control/Scan Rate",
            ),
        ]

        births = await self._read_births()
        scans = []
        for birth in births:
            if "Properties/" in birth.name:  # Properties will not be scanned
                continue

            scan_rate = self._scan_rate
            if "scan_rate" in birth.properties:
                scan_rate = birth.properties["scan_rate"].value
                if type(scan_rate) is not int:
                    raise ValueError(f"Scan rate can not be of type {type(scan_rate)}")

                if scan_rate == 0:  # No scan this metric
                    continue

            scans.append(
                _Scan(
                    scan_rate,
                    birth.datatype,
                    Quality(birth.properties["quality"].value),
                    birth.value,
                    alias=birth.alias,
                    name=birth.name,
                )
            )

        self._plan_scans(scans)

        return node_controls + births

    async def _scan_schedule(self, timestamp: int):
        wait_time = (timestamp - self._clock.timestamp()) / 1000
        await self._clock.asleep(wait_time if wait_time > 0 else 0)

        readings = await self._read_metrics(self._schedules[timestamp])
        self._report_changes(readings)
        self._plan_scans(self._schedules.pop(timestamp, []))
        if timestamp in self._tasks:
            self._tasks.pop(timestamp)

    async def _read_metrics(self, scans: list[_Scan]) -> list:
        readings = [
            asyncio.create_task(
                _Sample.read(self._net, self._clock, scan.name, scan.alias)
            )
            for scan in scans
        ]
        logger.debug(f"Scanning {len(readings)} metrics")

        timeout = self._scan_rate / 2000  #  half of scan rate
        try:
            _, pending = await asyncio.wait(
                readings,
                timeout=timeout,
            )
        except asyncio.CancelledError as e:
            for reading in readings:
                if not reading.done():
                    reading.cancel()
            raise e

        if pending:
            logger.warning(f"There are {len(pending)} staled readings by timeout")

        for reading in pending:
            reading.cancel()
        await asyncio.gather(*pending)

        changes = []
        for scan, reading in zip(scans, readings):
            metric = scan.update(reading.result())
            if metric is not None:
                changes.append(metric)

        return sorted(changes, key=lambda change: change.timestamp)

    def _report_changes(self, changes):
        if changes:
            self._queue.put_nowait(changes)
            logger.info(f"Reported {len(changes)} changes after scanning")
        else:
            logger.info("No changes to be reported after scanning")

    def _plan_scans(self, scans):
        for scan in scans:
            scan.plan_next_scan(self._schedules, self._clock)

        for timestamp in self._schedules.keys():
            if timestamp not in self._tasks:
                self._tasks[timestamp] = asyncio.create_task(
                    self._scan_schedule(timestamp)
                )

        logger.info(f"Planned to scan {len(scans)} metrics")

    async def stop(self):
        """Stop all next scanning tasks"""
        for task in self._tasks.values():
            task.cancel()
        await asyncio.gather(*list(self._tasks.values()), return_exceptions=True)
        self._tasks.clear()
        self._schedules.clear()

    def _find_scan(self, metric: Metric) -> _Scan | None:
        for scans in self._schedules.values():
            for scan in scans:
                if (metric.alias and metric.alias == scan.alias) or (
                    metric.name and metric.name == scan.metric_name
                ):
                    return scan

    async def execute_command(self, metric: Metric) -> Metric:
        """execute a command, writing metric to the net"""

        if metric.name == "Node Control/Scan Rate":
            if type(metric.value) is not int:
                raise ValueError(f"Metric {metric.name} has not type integer")
            self.scan_rate = metric.value
            return Metric(
                self._clock.timestamp(),
                metric.value,
                DataType.Int32,
                name="Node Control/Scan Rate",
            )

        try:
            await self._net.write_value(
                metric.value, metric_name=metric.name, alias=metric.alias
            )
            sample = _Sample(self._clock.timestamp(), metric.value, Quality.GOOD)
        except asyncio.CancelledError:
            sample = _Sample(self._clock.timestamp(), metric.value, Quality.STALE)
        except Exception as e:
            logger.error(
                f"Writing {metric.value} to metric '{metric.name}:{metric.alias}'"
            )
            logger.exception(e)
            sample = _Sample(self._clock.timestamp(), metric.value, Quality.BAD)

        scan = self._find_scan(metric)
        if scan:
            scan.update(sample)
        return Metric(
            sample.timestamp,
            metric.value,
            metric.datatype,
            metric.alias,
            metric.name,
            properties=PropertySet.from_dict(
                {"quality": {"value": sample.quality.value, "dataType": "Int32"}}
            ),
        )

    @scan_rate.setter
    def scan_rate(self, value: int):
        replanned_scans = []
        for timestamp in list(self._schedules.keys()):
            scans = []
            for scan in self._schedules.pop(timestamp):
                if scan.scan_rate == self._scan_rate:
                    replanned_scans.append(
                        _Scan(
                            value,
                            scan.datatype,
                            scan.quality,
                            scan.value,
                            scan.alias,
                            scan.name,
                        )
                    )
                else:
                    scans.append(scan)
            if scans:
                self._schedules[timestamp] = scans
            else:
                self._tasks.pop(timestamp).cancel()

        self._plan_scans(replanned_scans)
        self._scan_rate = value
