import abc
import asyncio
import logging
import re

from aiospb.mqtt import MqttClient
from aiospb.mqtt.encoding.json import JsonEncoder
from aiospb.mqtt.paho import PahoMqttClient
from aiospb.nodes import EdgeNode

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MqttServer:
    """Create mqtt clients working asyncronously"""

    def __init__(self, mqtt_config: dict[str, str]):
        self._config = mqtt_config
        self._encoder = JsonEncoder()

    def create_client(self) -> MqttClient:
        """Create an asyncronous mqtt client"""
        return PahoMqttClient(self._config, self._encoder)


class NodeFactory(abc.ABC):
    """Create connections to device from Nodes/Devices"""

    @property
    @abc.abstractmethod
    def node_names(self) -> list[str]:
        """Return all name of nodes available to connect by"""

    @abc.abstractmethod
    def create(self, name: str) -> EdgeNode:
        """Create a device connection"""


class NodesGroup:
    """Runnable class which manage a group of edge nodes"""

    def __init__(
        self,
        name: str,
        node_fry: NodeFactory,
        time_to_restart: int = 10,
        cicle_time: int = 2,
    ):
        self._name = name
        self._node_fry = node_fry
        self._filter = None
        self._nodes = []
        self._time_to_restart = time_to_restart
        self._cicle_time = cicle_time

    @property
    def name(self) -> str:
        """Return the name of the group"""
        return self._name

    @property
    def nodes(self) -> list[EdgeNode]:
        """Return all executable nodes."""
        return self._nodes.copy()

    def setup(self, nodes_filter: str = ""):
        pattern = re.compile(nodes_filter)
        for name in self._node_fry.node_names:
            if pattern.match(name):
                self._nodes.append(self._node_fry.create(name))

    async def _start_all_nodes(self, cycles: int = -1):
        for node in self._nodes:
            logger.info(f"Establishing session at node {node.name}")
            await node.establish_session()

        counter = 0
        while True:
            if cycles >= 0:
                counter += 1
            for node in self._nodes:
                if node.state == "crashed":
                    logger.warning(
                        f"Node '{node.name}' has crashed internally, terminating cleanly"
                    )
                    await node.terminate_session()
                    await asyncio.sleep(self._time_to_restart)

                    logger.info(f"Restablishing session at node {node.name}")
                    await node.establish_session()
            if cycles and counter == cycles:
                break
            await asyncio.sleep(self._cicle_time)

    def run(self, cycles: int = -1):
        """Run the group as an application in the OS"""
        asyncio.run(self._start_all_nodes(cycles))
