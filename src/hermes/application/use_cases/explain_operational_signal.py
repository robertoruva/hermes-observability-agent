from hermes.domain.operations import OperationalExplanation
from hermes.ports.metrics_reader import MetricsReader
from hermes.ports.operations_explainer import OperationsExplainer


class ExplainOperationalSignal:
    def __init__(
        self,
        metrics_reader: MetricsReader,
        operations_explainer: OperationsExplainer,
    ) -> None:
        self._metrics_reader = metrics_reader
        self._operations_explainer = operations_explainer

    def execute(self, signal_name: str) -> OperationalExplanation:
        for signal in self._metrics_reader.list_signals():
            if signal.name == signal_name:
                return self._operations_explainer.explain(signal)

        raise OperationalSignalNotFound(signal_name)


class OperationalSignalNotFound(ValueError):
    def __init__(self, signal_name: str) -> None:
        super().__init__(f"Operational signal not found: {signal_name}")
        self.signal_name = signal_name
