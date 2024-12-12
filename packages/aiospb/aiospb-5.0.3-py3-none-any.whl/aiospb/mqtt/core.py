import abc
from dataclasses import dataclass
from typing import Any, Self

from ..data import Metric


@dataclass
class Topic:
    value: str

    @property
    def component_name(self) -> str:
        items = self.value.split("/")
        if items[1] == "STATE":
            return "/".join(items[2:])
        else:
            return "/".join([items[1]] + items[3:])

    @property
    def message_type(self) -> str:
        items = self.value.split("/")
        if items[1] == "STATE":
            return "STATE"
        return items[2]

    @classmethod
    def from_component(cls, name: str, message_type: str) -> Self:
        if message_type not in (
            "STATE",
            "NDATA",
            "NBIRTH",
            "NDEATH",
            "NCMD",
            "DDATA",
            "DBIRTH",
            "DDEATH",
        ):
            raise ValueError(f'Message type "{message_type}" is not a standard')
        if message_type == "STATE":
            return cls(f"spBv1.0/STATE/{name}")
        items = name.split("/")
        return cls(f"spBv1.0/{items[0]}/{message_type}/{'/'.join(items[1:])}")


@dataclass
class Payload(abc.ABC):
    timestamp: int

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, payload_map: dict[str, Any]) -> Self:
        """Create a payload from a plain dict"""

    @abc.abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for parsing"""


@dataclass
class SpbMessage:
    topic: Topic
    payload: Payload

    def is_a(self, message_type: str) -> bool:
        return message_type == self.topic.message_type

    def is_from_node(self) -> bool:
        return "STATE" != self.topic.message_type


@dataclass
class Will:
    """Will message to sent to MQTT broker"""

    message: SpbMessage
    qos: int
    retain: bool


class MqttClient(abc.ABC):
    @property
    @abc.abstractmethod
    def is_connected(self) -> bool:
        """Is the client connected to the Broker?"""

    @abc.abstractmethod
    async def connect(self, component_name: str, will: Will):
        """Connect a component to MQTT server"""

    @abc.abstractmethod
    async def publish(self, message: SpbMessage, qos: int, retain: bool):
        """Publish a message  to the topic"""

    @abc.abstractmethod
    async def deliver_message(self) -> SpbMessage:
        """Return a messsage recieved from the MQTT Server"""

    @abc.abstractmethod
    async def subscribe(self, topic: str, qos: int):
        """Subscribe the component to recieve messages from a topic"""

    @abc.abstractmethod
    async def disconnect(self, component_name: str, will_reason: str = ""):
        """Disconnect the client from the MQTT server"""


@dataclass
class HostPayload(Payload):
    """Payload to send by MQTT for State messages"""

    online: bool

    @classmethod
    def from_dict(cls, payload_map: dict[str, Any]) -> Self:
        """Create a payload from a plain dict"""
        return cls(payload_map["timestamp"], payload_map["online"])

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for parsing"""
        return {"timestamp": self.timestamp, "online": self.online}


@dataclass
class MessageContent(abc.ABC):
    """Interface of a message content"""

    @abc.abstractmethod
    async def send(
        self,
        mqtt_client: "MqttClient",
        timestamp: int,
        component_name: str,
        seq: int | None = None,
    ):
        """Publish to MQTT Broker the content of the message"""


@dataclass
class NodePayload(Payload):
    """Payload to send by MQTT for/to edge node messages"""

    metrics: list[Metric]
    seq: int | None = None

    @classmethod
    def from_dict(cls, payload_map: dict[str, Any]) -> Self:
        """Create a payload from a plain dict"""
        return cls(
            payload_map["timestamp"],
            [Metric.from_dict(value) for value in payload_map["metrics"]],
            payload_map.get("seq"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for parsing"""
        outcome = {
            "timestamp": self.timestamp,
            "metrics": [dto.as_dict() for dto in self.metrics],
        }
        if self.seq is not None:
            outcome["seq"] = self.seq

        return outcome


@dataclass
class MqttConfig:
    hostname: str
    port: int
    username: str | None = None
    password: str | None = None
    ca_certs: str = ""
    keepalive: int = 30


class MessageEncoder(abc.ABC):
    """Encode the message before sending it as payload in the message"""

    @abc.abstractmethod
    def encode(self, payload: Payload) -> bytes:
        """Convert a message to a payload"""

    @abc.abstractmethod
    def decode(self, payload: bytes) -> Payload:
        """Convert payload to a message object"""


class MqttError(Exception):
    """Wraps error of comunications by any MQTT adapter"""
