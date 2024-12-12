from typing import Any

import aiomqtt

from . import MqttClient, MqttConfig, MqttError, SpbMessage, Topic, Will
from .encoding import JsonEncoder, ProtobufEncoder


class PahoMqttClient(MqttClient):
    def __init__(
        self,
        config: dict[str, Any],
    ):
        config["port"] = int(config["port"])
        config["keepalive"] = int(config.get("keepalive", 30))
        self._config = MqttConfig(**config)

        self._client = None
        self._json_encoder = JsonEncoder()
        self._protobuf_encoder = ProtobufEncoder()
        self._is_host = None

    async def connect(self, component_name: str, will: Will):
        payload = self._encode_message(will.message)
        will_ = aiomqtt.Will(
            will.message.topic.value, payload, qos=will.qos, retain=will.retain
        )

        tls_pars = None
        if self._config.ca_certs:
            tls_pars = aiomqtt.TLSParameters(ca_certs=self._config.ca_certs)

        self._client = aiomqtt.Client(
            self._config.hostname,
            self._config.port,
            identifier=component_name,
            username=self._config.username,
            password=self._config.password,
            will=will_,
            protocol=aiomqtt.ProtocolVersion.V5,
            tls_params=tls_pars,
            clean_start=True,
            keepalive=self._config.keepalive,
        )

        try:
            await self._client.__aenter__()  # Connect with aiomqtt
        except Exception as e:
            self._client = None
            raise MqttError() from e

    @property
    def keepalive(self) -> float:
        return self._config.keepalive

    @property
    def is_connected(self) -> bool:
        return self._client is not None

    def _encode_message(self, message: SpbMessage) -> bytes:
        if message.topic.value.startswith("spBv1.0/STATE/"):
            return self._json_encoder.encode(message.payload)

        return self._protobuf_encoder.encode(message.payload)

    async def publish(self, message: SpbMessage, qos: int, retain: bool):
        if self._client is None:
            raise RuntimeError("Client not connected to Mqtt Server")

        try:
            await self._client.publish(
                message.topic.value,
                self._encode_message(message),
                qos=qos,
                retain=retain,
            )
        except Exception as e:
            self._client = None
            raise MqttError() from e

    async def subscribe(self, topic: str, qos: int):
        if self._client is None:
            raise RuntimeError("Client not connected to Mqtt Server")

        try:
            await self._client.subscribe(topic, qos=qos)
        except Exception as e:
            self._client = None
            raise MqttError() from e

    async def deliver_message(self) -> SpbMessage:
        if self._client is None:
            raise RuntimeError("Mqtt client is not connected")

        try:
            message = await anext(self._client.messages)
        except Exception as e:
            self._client = None
            raise MqttError() from e

        # if type(message.payload) is not bytes:
        #     raise ValueError(f"Message should be bytes {message.payload}")

        if message.topic.value.startswith("spBv1.0/STATE/"):
            return SpbMessage(
                Topic(message.topic.value), self._json_encoder.decode(message.payload)
            )

        message = SpbMessage(
            Topic(message.topic.value), self._protobuf_encoder.decode(message.payload)
        )

        return message

    async def disconnect(self):
        if self._client is None:
            return

        await self._client.__aexit__(None, None, None)
        self._client = None
