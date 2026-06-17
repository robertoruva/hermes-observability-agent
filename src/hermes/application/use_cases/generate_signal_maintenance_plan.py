from hermes.application.use_cases.explain_operational_signal import (
    ExplainOperationalSignal,
)
from hermes.domain.maintenance import MaintenancePlan
from hermes.ports.maintenance_planner import MaintenancePlanner
from hermes.ports.metrics_reader import MetricsReader
from hermes.ports.operations_explainer import OperationsExplainer


class GenerateSignalMaintenancePlan:
    def __init__(
        self,
        metrics_reader: MetricsReader,
        operations_explainer: OperationsExplainer,
        maintenance_planner: MaintenancePlanner,
    ) -> None:
        self._metrics_reader = metrics_reader
        self._operations_explainer = operations_explainer
        self._maintenance_planner = maintenance_planner

    def execute(self, signal_name: str) -> MaintenancePlan:
        explanation = ExplainOperationalSignal(
            self._metrics_reader,
            self._operations_explainer,
        ).execute(signal_name)
        return self._maintenance_planner.generate_plan([explanation])
