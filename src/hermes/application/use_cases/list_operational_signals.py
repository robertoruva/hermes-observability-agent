from hermes.domain.metrics import OperationalSignal
from hermes.ports.metrics_reader import MetricsReader


class ListOperationalSignals:
    def __init__(self, metrics_reader: MetricsReader) -> None:
        self._metrics_reader = metrics_reader

    def execute(self) -> list[OperationalSignal]:
        return self._metrics_reader.list_signals()
