"""Main components of sparkplug standard"""
import logging

from aiospb.nodes.messages import MqttNodeCarrier

from .scanning import Scanner
from .states import Disconnected, NodeContext
from .stores import HistoricalStore

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MetricsConnectionError(Exception):
    ...


class EdgeNode:
    """Gateway connected to mqtt and to one or more hardware devices"""

    def __init__(
        self,
        name: str,
        mqtt_carrier: MqttNodeCarrier,
        scanner: Scanner,
        store: HistoricalStore,
        primary_hostname: str = "",
    ):
        self._name = name
        self._carrier = mqtt_carrier
        self._scanner = scanner
        self._store = store
        self._primary_hostname = primary_hostname
        self._context = NodeContext(
            self._carrier,
            self._scanner,
            self._store,
            self._primary_hostname,
        )
        self._context.state = Disconnected(self._context)

    @property
    def name(self) -> str:
        return self._name

    @property
    def state(self) -> str | None:
        if self._context is None:
            return
        return self._context.state.__class__.__name__.lower()

    async def establish_session(self):
        """Establish a session for a supplied metrics net"""
        if self._context.state is None:  # pragma: no cover
            return

        await self._context.state.establish_session()

    async def terminate_session(self):
        """Terminate cleanly the session and"""
        if self._context.state is None:  # pragma: no cover
            return

        await self._context.state.terminate_session()
