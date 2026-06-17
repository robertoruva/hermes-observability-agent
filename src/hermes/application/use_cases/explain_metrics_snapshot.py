from hermes.domain.operations import OperationalExplanation
from hermes.ports.metrics_reader import MetricsReader
from hermes.ports.operations_explainer import OperationsExplainer


class ExplainMetricsSnapshot:
    def __init__(
        self,
        metrics_reader: MetricsReader,
        operations_explainer: OperationsExplainer,
    ) -> None:
        self._metrics_reader = metrics_reader
        self._operations_explainer = operations_explainer

    def execute(self) -> list[OperationalExplanation]:
        return [
            self._operations_explainer.explain(signal)
            for signal in self._metrics_reader.list_signals()
        ]
