"""A MQTT Server can not warrant that host application would recieve the node messages
in the same order is sent. If not, standards rules a rebirth"""
import asyncio
import logging

from aiospb import Clock, UtcClock
from aiospb.data import DataType, Metric, WriteRequest
from aiospb.mqtt import (
    HostPayload,
    MqttClient,
    MqttError,
    NodePayload,
    SpbMessage,
    Topic,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NodeMessageSorter:
    def __init__(
        self,
        node_name: str,
        clock: Clock,
        reorder_time: float = 2.0,  # in s
    ):
        self._node_name = node_name
        self._clock = clock
        self._reorder_time = reorder_time

        self._seq = -1
        self._bd_seq = -1
        self._messages = {}
        self._timeout_ts = 0

    def register_message(self, message: SpbMessage):
        if type(message.payload) is not NodePayload:
            return

        if message.is_a("NCMD"):
            return

        if message.is_a("NDATA") and self._seq == -1:
            logger.warning(f"Lost of data by no birth at {self._node_name}")
            return

        if message.is_a("NDEATH"):
            if message.payload.metrics[0].value == self._bd_seq:
                self._messages[None] = message
            return

        if message.is_a("NBIRTH"):
            self._messages.clear()

            bd_seq = None
            for metric in message.payload.metrics:
                if metric.name == "bdSeq":
                    bd_seq = metric.value

            if bd_seq is None:
                raise ValueError(f"Birth from {self._node_name} has not bdSeq!!")

            if bd_seq != self._bd_seq:
                self._bd_seq = bd_seq
                self._seq = message.payload.seq
                self._messages.clear()

        self._messages[message.payload.seq] = message

    def nexts(self) -> list[SpbMessage]:
        output = []
        while self._messages:
            if self._seq in self._messages:
                output.append(self._messages.pop(self._seq))
                self._seq = 0 if self._seq == 255 else self._seq + 1
                self._timeout_ts = self._clock.timestamp() + self._reorder_time * 1000
            elif None in self._messages:
                message = self._messages.pop(None)
                output.append(message)
                self._messages.clear()
                self._seq = -1
            else:
                if self._clock.timestamp() > self._timeout_ts:
                    self._messages.clear()
                    logger.warning(
                        f"There are {len(self._messages)} messages disordered too much time in {self._node_name}"
                    )
                    raise TimeoutError()
                break
        return output
