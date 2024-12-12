import asyncio
import logging
from typing import Callable, Coroutine, Sequence

from aiospb import Clock, UtcClock
from aiospb.data import DataType, Metric, WriteRequest
from aiospb.mqtt import (
    HostPayload,
    MqttClient,
    MqttError,
    NodePayload,
    SpbMessage,
    Topic,
    Will,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class _Observer:
    def __init__(self, callback: Callable, filter: str = ""):
        self.callback = callback
        self._filter = filter

    async def notify(self, message: SpbMessage):
        if not self._filter or self._filter in message.topic.component_name:
            await self.callback(message)


class _MessageSorter:
    def __init__(self, node_name: str, clock: Clock, reorder_time: float = 2.0):
        self._name = node_name
        self._next_seq = 0
        self._clock = clock
        self._bd_seq = 0
        self._reorder_time = int(reorder_time * 1000)  # ms
        self._messages = {}
        self._timeout = 0

    def register_message(self, message: SpbMessage):
        content = message.payload.to_dict()
        if message.is_a("NCMD"):
            return

        if message.is_a("NDEATH"):
            self._messages[None] = message
            return

        seq = content["seq"]
        if message.is_a("NBIRTH"):
            self._messages.clear()
            self._next_seq = seq
            self._bd_seq = self._get_bd_seq(content["metrics"])

        self._messages[seq] = message

    def _get_bd_seq(self, metrics):
        for metric in metrics:
            if metric.get("name") == "bdSeq":
                return metric["value"]

    def nexts(self) -> list[SpbMessage]:
        output = []
        while self._messages:
            if self._next_seq in self._messages:
                output.append(self._messages.pop(self._next_seq))
                self._next_seq = 0 if self._next_seq == 255 else self._next_seq + 1
                self._timeout = self._clock.timestamp() + self._reorder_time
            elif None in self._messages:
                message = self._messages.pop(None)
                if message.payload.to_dict()["metrics"][0]["value"] != self._bd_seq:
                    continue

                output.append(message)
                self._messages.clear()
                self._next_seq = 0
            else:
                if self._clock.timestamp() > self._timeout:
                    self._messages.clear()
                    raise TimeoutError(
                        f"There are {len(self._messages)} messages disordered too much time"
                    )
                break
        return output


class _NodeCommander:
    def __init__(self, node_name, mqtt_client, clock):
        self._datatypes = {}
        self._aliases = {}
        self._clock = clock
        self._node_name = node_name
        self._mqtt_client = mqtt_client
        self._pending_commands = {}

    async def notify(self, message: SpbMessage):
        if message.is_a("NBIRTH"):
            metrics = message.payload.to_dict()["metrics"]

            self._datatypes.clear()
            for metric in metrics:
                datatype = (
                    DataType[metric["dataType"]]
                    if type(metric["dataType"]) is str
                    else DataType(metric["dataType"])
                )
                if "alias" in metric:
                    self._datatypes[metric["alias"]] = datatype
                    self._aliases[metric["name"]] = metric["alias"]
                self._datatypes[metric["name"]] = datatype
        elif message.is_a("NDATA"):
            metrics = message.payload.to_dict()["metrics"]
            self._clear_expired_commands()

            changes = [
                (data["value"], data.get("name", ""), data.get("alias", 0))
                for data in metrics
            ]

            for expected_changes, samples in self._pending_commands.values():
                if expected_changes == changes:
                    samples.set_result([Metric.from_dict(data) for data in metrics])

    def _clear_expired_commands(self):
        now = self._clock.timestamp()

        for ts in list(self._pending_commands.keys()):
            if now > ts:
                self._pending_commands.pop(ts)

    async def write_metrics(
        self, requests: Sequence[WriteRequest], timeout
    ) -> list[Metric]:
        logger.info(
            f'Requesting {len(requests)} metric changes to edge node "{self._node_name}"...'
        )
        changes = await self._send_command(requests)
        logger.debug("Command sent to edge node")
        if not changes:
            return []

        ts = self._clock.timestamp() + int(1000 * timeout)
        samples = asyncio.Future()
        self._pending_commands[ts] = (changes, samples)
        logger.debug(f"Waiting confirmation by node {self._node_name}...")
        metrics = await asyncio.wait_for(samples, timeout=timeout)
        logger.info(f'Recieved feedback of writing in "{self._node_name}"')
        for metric in metrics:
            logger.debug(f"Metric confirmation by {self._node_name} is: {metric}")
        return metrics

    async def _send_command(self, requests):
        ts = self._clock.timestamp()
        metrics = []
        for request in requests:
            alias = request.alias
            name = request.metric_name
            if alias not in self._aliases.values() and name not in self._datatypes:
                continue
            datatype = self._datatypes.get(alias) or self._datatypes[name]

            if name in self._aliases:
                alias = self._aliases[name]
                name = ""

            metrics.append(Metric(ts, request.value, datatype, alias, name))

        if not metrics:
            return []

        await self._mqtt_client.publish(
            SpbMessage(
                Topic.from_component(self._node_name, "NCMD"), NodePayload(ts, metrics)
            ),
            qos=0,
            retain=False,
        )
        return [(metric.value, metric.name, metric.alias) for metric in metrics]


class HostBridge:
    """Easy interface to host applications"""

    def __init__(
        self,
        hostname: str,
        mqtt_client: MqttClient,
        groups: str = "",
        reorder_timeout: float = 2,
        max_delay: int = 10,
        clock: Clock | None = None,
    ):
        self._hostname = hostname
        self._groups = groups.split(",")
        self._mqtt_client = mqtt_client
        self._reorder_timeout = reorder_timeout
        self._max_delay = max_delay
        self._clock = clock if clock else UtcClock()

        self._observers = []
        self._state = "offline"
        self._recieving = None
        self._listen_nodes = None
        self._sorters = {}
        self._commanders = {}

    @property
    def hostname(self) -> str:
        """Name of the host application"""
        return self._hostname

    @property
    def state(self):
        return self._state

    async def establish_session(self, groups: list[str] | None = None):
        """Init session to listen edge nodes"""

        await self._mqtt_client.connect(
            self._hostname,
            will=Will(
                SpbMessage(
                    Topic.from_component(self._hostname, "STATE"),
                    HostPayload(self._clock.timestamp(), False),
                ),
                qos=1,
                retain=True,
            ),
        )
        groups = groups or ["+"]
        for group in groups:
            await self._mqtt_client.subscribe(f"spBv1.0/{group}/+/+", qos=1)

        self._recieving = asyncio.create_task(self._recieve_node_messages())

        await self._mqtt_client.publish(
            SpbMessage(
                Topic.from_component(self._hostname, "STATE"),
                HostPayload(self._clock.timestamp(), True),
            ),
            qos=1,
            retain=True,
        )
        logger.info(f'Host application "{self._hostname}" has established session')
        self._state = "online"

    async def terminate_session(self):
        """Close cleanly a session"""

        if self._recieving is not None:
            self._recieving.cancel()

        try:
            await self._mqtt_client.publish(
                SpbMessage(
                    Topic.from_component(self._hostname, "STATE"),
                    HostPayload(self._clock.timestamp(), False),
                ),
                qos=1,
                retain=True,
            )
            await self._mqtt_client.disconnect()
        except MqttError as e:
            logger.error("MQTT connection broken when terminating session")
            logger.exception(e)

    def done(self):
        return self._listen_nodes is None or self._listen_nodes.done()

    def observe_nodes(
        self,
        callback: Callable[[SpbMessage], Coroutine[None, None, None]],
        node_filter: str = "",
    ) -> None:
        """Add one callable observer when it rece"""

        self._observers.append(_Observer(callback, node_filter))

    async def _recieve_node_messages(self):
        while True:
            try:
                message: SpbMessage = await self._mqtt_client.deliver_message()
                if not message.is_from_node():
                    continue

                node_name = message.topic.component_name
                if node_name not in self._sorters:
                    self._commanders[node_name] = commander = _NodeCommander(
                        node_name, self._mqtt_client, self._clock
                    )
                    self._observers.append(_Observer(commander.notify, node_name))

                    self._sorters[node_name] = _MessageSorter(
                        node_name, self._clock, self._reorder_timeout
                    )
                sorter = self._sorters[node_name]
                sorter.register_message(message)

                try:
                    for message in sorter.nexts():
                        results = await asyncio.gather(
                            *[observer.notify(message) for observer in self._observers],
                            return_exceptions=True,
                        )
                        for result, observer in zip(results, self._observers):
                            if type(result) is Exception:
                                logger.warning(
                                    f"Observer {observer} raised exception when notified"
                                )
                                logger.exception(result)
                except TimeoutError:
                    ts = self._clock.timestamp()
                    await self._mqtt_client.publish(
                        SpbMessage(
                            Topic.from_component(node_name, "NCMD"),
                            NodePayload(
                                ts,
                                metrics=[
                                    Metric(
                                        ts,
                                        True,
                                        DataType.Boolean,
                                        name="Node Control/Rebirth",
                                    )
                                ],
                            ),
                        ),
                        qos=0,
                        retain=False,
                    )

            except Exception as e:
                logger.error("Task of recieving node messages has stopped")
                logger.exception(e)
                raise e

    async def write_metrics(
        self, node_name: str, write_requests: list[WriteRequest], timeout: float = 10.0
    ):
        """Request changes to metrics"""

        try:
            return await self._commanders[node_name].write_metrics(
                write_requests, timeout
            )

        except TimeoutError as e:
            logger.warning(
                f"Not recieved confirmation of writing for {timeout} seconds"
            )
            raise e
        except Exception as e:
            logger.error(
                f"Request of metrics changes at {node_name} has been stopped by exception"
            )
            logger.exception(e)
            raise e
