from hermes.application.use_cases.generate_signal_maintenance_plan import (
    GenerateSignalMaintenancePlan,
)
from hermes.domain.actions import ActionProposal
from hermes.ports.action_proposer import ActionProposer
from hermes.ports.maintenance_planner import MaintenancePlanner
from hermes.ports.metrics_reader import MetricsReader
from hermes.ports.operations_explainer import OperationsExplainer


class ProposeSignalActions:
    def __init__(
        self,
        metrics_reader: MetricsReader,
        operations_explainer: OperationsExplainer,
        maintenance_planner: MaintenancePlanner,
        action_proposer: ActionProposer,
    ) -> None:
        self._metrics_reader = metrics_reader
        self._operations_explainer = operations_explainer
        self._maintenance_planner = maintenance_planner
        self._action_proposer = action_proposer

    def execute(self, signal_name: str) -> list[ActionProposal]:
        plan = GenerateSignalMaintenancePlan(
            self._metrics_reader,
            self._operations_explainer,
            self._maintenance_planner,
        ).execute(signal_name)
        return self._action_proposer.propose_actions(plan)
