import asyncio
import logging
from dataclasses import dataclass
from enum import Enum

from aiospb import Clock
from aiospb.data import DataType, Metric, Quality, ValueType, WriteRequest
from aiospb.mqtt import MqttClient, MqttError, NodePayload, SpbMessage, Topic
from aiospb.mqtt.core import MqttClient, NodePayload, SpbMessage

logger = logging.getLogger(__name__)


@dataclass
class CommandRequest:
    requests: list[WriteRequest]
    writing_timeout: float = 60.0


class WritingResolution(Enum):
    BadWriting = 0
    EdgeIsOffline = 5
    HostIsOffline = 10
    MetricNotFound = 15
    GoodWriting = 192
    StaleWriting = 500
    WritingTimeout = 505


@dataclass
class CommandResponse:
    timestamp: int
    resolutions: list[WritingResolution]


class _CommandTrack:
    def __init__(self, metric_ids: list[int | str], values: list[ValueType]):
        self.metric_ids = metric_ids
        self.values = values
        self.has_finished = asyncio.Event()
        self.resolutions = [WritingResolution.WritingTimeout] * len(values)

    def confirm_change(self, metric: Metric):
        index = None

        if metric.alias:
            try:
                index = self.metric_ids.index(metric.alias)
            except ValueError:
                pass

        if index is None:
            try:
                index = self.metric_ids.index(metric.name)
            except ValueError:
                return

        if self.values[index] != metric.value:
            return

        if "quality" in metric.properties:
            self.resolutions[index] = WritingResolution(metric.properties["quality"])

        if WritingResolution.WritingTimeout not in self.resolutions:
            self.has_finished.set()


class NodeCommander:
    def __init__(self, node_name: str, mqtt_client: MqttClient, clock: Clock):
        self._node_name = node_name
        self._mqtt_client = mqtt_client
        self._clock = clock
        self._aliases = {}
        self._datatypes = {}
        self._tracks = {}
        self._resolutions = {}
        self._is_online = False

    def handle_node_message(self, message: SpbMessage):
        """Update info of open commands"""
        if type(message.payload) is not NodePayload:
            return

        if message.is_a("NBIRTH"):
            self._is_online = True
            self._aliases.clear()
            self._datatypes.clear()
            for metric in message.payload.metrics:
                if "Properties" in metric.name:
                    continue
                if metric.alias:
                    self._aliases[metric.name] = metric.alias
                    self._datatypes[metric.alias] = metric.datatype
                else:
                    self._datatypes[metric.name] = metric.datatype
            return

        if message.is_a("NDATA"):
            if self._datatypes:
                logger.warning(
                    (
                        f"Recieved {len(message.payload.metrics)} without birth"
                        f" from {self._node_name}, ignoring..."
                    )
                )

            for metric in message.payload.metrics:
                for track in self._tracks.values():
                    track.confirm_change(metric)

        if message.is_a("NDEATH"):
            self._is_online = False

    async def execute(self, request: CommandRequest) -> CommandResponse:
        """Execute a command request"""
        n_writes = len(request.requests)
        if not self._is_online:
            return CommandResponse(
                self._clock.timestamp(),
                [WritingResolution.EdgeIsOffline] * n_writes,
            )

        try:
            timestamp = self._clock.timestamp()
            await self._send_command(timestamp, request.requests)
        except MqttError:
            return CommandResponse(
                self._clock.timestamp(), [WritingResolution.HostIsOffline] * n_writes
            )

        try:
            await asyncio.wait_for(
                self._tracks[timestamp].has_finished.wait(),
                timeout=request.writing_timeout - timestamp,
            )
        except TimeoutError:
            pass

        return CommandResponse(
            self._clock.timestamp(), self._tracks.pop(timestamp).resolutions
        )

    async def _send_command(self, timestamp: int, requests: list[WriteRequest]):
        metrics = []
        metric_ids = []
        values = []

        not_found_metrics = []
        for index, request in enumerate(requests):
            name = ""
            alias = 0

            if request.metric_name and request.metric_name in self._aliases:
                alias = self._aliases[request.metric_name]

            if request.alias and request.alias in self._aliases.values():
                alias = request.alias

            if not alias and request.metric_name in self._datatypes:
                name = request.metric_name

            metric_ids.append(alias or name)
            values.append(request.value)

            if not alias and not name:
                not_found_metrics.append(index)
                continue

            datatype = self._datatypes.get(alias) or self._datatypes[name]
            metrics.append(Metric(timestamp, request.value, datatype, alias, name))

        if metrics:
            await self._mqtt_client.publish(
                SpbMessage(
                    Topic.from_component(self._node_name, "NCMD"),
                    NodePayload(timestamp, metrics),
                ),
                qos=0,
                retain=False,
            )

        track = _CommandTrack(metric_ids, values)
        if not_found_metrics:
            for index in not_found_metrics:
                track.resolutions[index] = WritingResolution.MetricNotFound

        if WritingResolution.WritingTimeout not in track.resolutions:
            track.has_finished.set()

        self._tracks[timestamp] = track
