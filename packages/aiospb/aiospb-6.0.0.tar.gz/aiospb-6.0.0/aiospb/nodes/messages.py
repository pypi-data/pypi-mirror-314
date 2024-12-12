import logging

from .. import Clock, UtcClock
from ..data import DataType, Metric
from ..mqtt import MqttClient, NodePayload, SpbMessage, Topic, Will

logger = logging.getLogger(__name__)


class _Seq:
    """Rotatory sequency number from 0 to 255"""

    def __init__(self):
        self._value = None

    def __call__(self) -> int:
        """If it is called, the previous value is increased and return it"""
        if self._value is None:
            self._value = 0
            return self._value

        self._value = 0 if self._value == 255 else self._value + 1
        return self._value

    @property
    def value(self) -> int:
        """Return their value (not increasing)"""
        if self._value is None:
            raise RuntimeError("Sequence not initialized")

        return self._value


class MqttNodeCarrier:
    """Helper to send Node messages to mqtt"""

    def __init__(
        self,
        mqtt_client: MqttClient,
        node_name: str,
        clock: Clock | None = None,
    ):
        self._mqtt_client = mqtt_client
        self._node_name = node_name
        self._clock = clock or UtcClock()
        self._seq = None
        self._bd_seq = _Seq()

    async def connect(self):
        """Connect node to MQTT Server"""
        ts = self._clock.timestamp()
        will = Will(
            SpbMessage(
                Topic.from_component(self._node_name, "NDEATH"),
                NodePayload(
                    timestamp=ts,
                    metrics=[Metric(ts, self._bd_seq(), DataType.Int64, name="bdSeq")],
                ),
            ),
            qos=1,
            retain=False,
        )
        self._seq = _Seq()

        await self._mqtt_client.connect(self._node_name, will=will)
        await self._mqtt_client.subscribe("spBv1.0/STATE/+", qos=1)
        await self._mqtt_client.subscribe(
            Topic.from_component(self._node_name, "NCMD").value, qos=1
        )

    async def send_birth(self, metrics: list[Metric]):
        """Send birth certificate"""
        if self._seq is None:
            raise RuntimeError("The node is not connected yet")

        ts = self._clock.timestamp()
        await self._mqtt_client.publish(
            SpbMessage(
                Topic.from_component(self._node_name, "NBIRTH"),
                NodePayload(
                    ts,
                    metrics
                    + [Metric(ts, self._bd_seq.value, DataType.Int64, name="bdSeq")],
                    self._seq(),
                ),
            ),
            qos=0,
            retain=False,
        )

    async def send_data_changes(self, metrics: list[Metric]):
        """Send metrics changes to MQTT Server"""
        if self._seq is None:
            raise RuntimeError("The node is not connected yet")

        await self._mqtt_client.publish(
            SpbMessage(
                Topic.from_component(self._node_name, "NDATA"),
                NodePayload(self._clock.timestamp(), metrics, self._seq()),
            ),
            qos=0,
            retain=False,
        )

    async def send_death(self):
        """Send death certificate to MQTT Server"""
        if self._seq is None:
            raise RuntimeError("The node is not connected yet")

        ts = self._clock.timestamp()
        await self._mqtt_client.publish(
            SpbMessage(
                Topic.from_component(self._node_name, "NDEATH"),
                NodePayload(
                    ts,
                    [Metric(ts, self._bd_seq.value, DataType.Int64, name="bdSeq")],
                ),
            ),
            qos=1,
            retain=False,
        )

    async def confirm_commands(self, writings: list[Metric]):
        """Send confirmation of commands to the MQTT Server"""
        if self._seq is None:
            raise RuntimeError("The node is not connected yet")

        metrics = []
        for writing in writings:
            if writing.timestamp == 0:
                metrics.append(
                    Metric(
                        self._clock.timestamp(),
                        writing.value,
                        writing.datatype,
                        writing.alias,
                        writing.name,
                        writing.properties,
                    )
                )
                continue
            metrics.append(writing)

        await self._mqtt_client.publish(
            SpbMessage(
                Topic.from_component(self._node_name, "NDATA"),
                NodePayload(self._clock.timestamp(), metrics, self._seq()),
            ),
            qos=0,
            retain=False,
        )

    async def disconnect(self):
        """Disconnect from MQTT Server"""
        await self._mqtt_client.disconnect()

    async def deliver_message(self) -> SpbMessage:
        """Return message content from MQTT Server"""
        return await self._mqtt_client.deliver_message()

    @property
    def is_connected(self):
        return self._mqtt_client.is_connected
