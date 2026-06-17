from hermes.domain.actions import ActionProposal
from hermes.ports.action_proposer import ActionProposer
from hermes.ports.maintenance_planner import MaintenancePlanner
from hermes.ports.metrics_reader import MetricsReader
from hermes.ports.operations_explainer import OperationsExplainer


class ProposeMaintenanceActions:
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

    def execute(self) -> list[ActionProposal]:
        explanations = [
            self._operations_explainer.explain(signal)
            for signal in self._metrics_reader.list_signals()
        ]
        plan = self._maintenance_planner.generate_plan(explanations)
        return self._action_proposer.propose_actions(plan)
