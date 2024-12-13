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

from .commands import CommandRequest, CommandResponse, NodeCommander, WritingResolution
from .sorting import NodeMessageSorter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class _Observer:
    def __init__(self, callback: Callable, filter: str = ""):
        self.callback = callback
        self._filter = filter

    async def notify(self, message: SpbMessage):
        if not self._filter or self._filter in message.topic.component_name:
            await self.callback(message)


class HostBridge:
    """Easy interface to host applications"""

    def __init__(
        self,
        hostname: str,
        mqtt_client: MqttClient,
        groups: str = "",
        reorder_timeout: float = 2,
        clock: Clock | None = None,
    ):
        self._hostname = hostname
        self._groups = groups.split(",")
        self._mqtt_client = mqtt_client
        self._reorder_timeout = reorder_timeout
        self._clock = clock if clock else UtcClock()

        self._observers = []
        self._is_online = False
        self._recieving = None
        self._sorters = {}
        self._commanders = {}

    @property
    def hostname(self) -> str:
        """Name of the host application"""
        return self._hostname

    @property
    def is_online(self) -> bool:
        return self._is_online

    async def establish_session(self, groups: list[str] | None = None):
        """Init session to listen edge nodes"""

        try:
            await self._connect()
            groups = groups or ["+"]
            await self._subscribe(groups)
            self._recieving = asyncio.create_task(self._recieve_node_messages())
            await self._send_birth_certificate()
        except MqttError as e:
            logger.error("Error with the MQTT Server when establishing session")
            logger.exception(e)
            self._is_online = False
            raise e

        logger.info(f'Host application "{self._hostname}" has established session')
        self._is_online = True

    async def terminate_session(self):
        """Close cleanly a session"""
        if self._recieving is not None:
            self._recieving.cancel()

        try:
            await self._send_death_certificate()
        except MqttError as e:
            logger.error("MQTT connection broken while sending host death certificate")
            logger.exception(e)

        logger.info(f'Host application "{self._hostname}" has terminated session')
        self._is_online = False

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
                    self._commanders[node_name] = NodeCommander(
                        node_name, self._mqtt_client, self._clock
                    )
                    self._sorters[node_name] = NodeMessageSorter(
                        node_name, self._clock, self._reorder_timeout
                    )

                sorter = self._sorters[node_name]
                sorter.register_message(message)
                try:
                    for message in sorter.nexts():
                        self._commanders[node_name].handle_node_message(message)
                        await self._notify_message_to_observers(message)
                except TimeoutError:
                    await self._send_rebirth_command(node_name)
                    logger.info(
                        f"Sent rebirth command to {node_name} by lost of message order"
                    )
            except MqttError as e:
                logger.error(f"Error when recieving node messages")
                logger.exception(e)
                self._is_online = False
                return
            except Exception as e:
                logger.error("Unmanaged exception when recieving node messages")
                logger.exception(e)
                logger.critical("The host is stopping to recieve messages")
                self._is_online = False
                return

    async def write_metrics(
        self, node_name: str, write_requests: list[WriteRequest], timeout: float = 10.0
    ) -> CommandResponse:
        """Request changes to metrics"""
        return await self._commanders[node_name].execute(
            CommandRequest(write_requests, timeout)
        )

    async def _notify_message_to_observers(self, message):
        results = await asyncio.gather(
            *[observer.notify(message) for observer in self._observers],
            return_exceptions=True,
        )
        for result, observer in zip(results, self._observers):
            if type(result) is Exception:
                logger.warning(f"Observer {observer} raised exception when notified")
                logger.exception(result)

    async def _connect(self):
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

    async def _subscribe(self, groups):
        for group in groups:
            await self._mqtt_client.subscribe(f"spBv1.0/{group}/+/+", qos=1)

    async def _send_birth_certificate(self):
        await self._mqtt_client.publish(
            SpbMessage(
                Topic.from_component(self._hostname, "STATE"),
                HostPayload(self._clock.timestamp(), True),
            ),
            qos=1,
            retain=True,
        )

    async def _send_rebirth_command(self, node_name):
        ts = self._clock.timestamp()
        message = SpbMessage(
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
        )
        await self._mqtt_client.publish(
            message,
            qos=0,
            retain=False,
        )

    async def _send_death_certificate(self):
        await self._mqtt_client.publish(
            SpbMessage(
                Topic.from_component(self._hostname, "STATE"),
                HostPayload(self._clock.timestamp(), False),
            ),
            qos=1,
            retain=True,
        )
        await self._mqtt_client.disconnect()
