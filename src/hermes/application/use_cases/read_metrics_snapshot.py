from hermes.domain.metrics import MetricsSnapshot
from hermes.ports.metrics_reader import MetricsReader


class ReadMetricsSnapshot:
    def __init__(self, metrics_reader: MetricsReader) -> None:
        self._metrics_reader = metrics_reader

    def execute(self) -> MetricsSnapshot:
        return self._metrics_reader.read_snapshot()
