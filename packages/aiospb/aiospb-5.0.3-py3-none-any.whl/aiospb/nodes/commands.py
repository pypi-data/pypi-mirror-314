from aiospb import Clock, UtcClock
from aiospb.nodes.ndata import Metric
from aiospb.nodes import MetricsNet


class NodeCommander:
    def __init__(self, metrics_net: MetricsNet, clock: Clock | None):
        self._net = metrics_net
        self._clock = clock or UtcClock()

    async def write_metric(self, metric: Metric):
        """Write a metric to the net"""
