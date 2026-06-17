import unittest

from hermes.application.use_cases.explain_operational_signal import (
    OperationalSignalNotFound,
)
from hermes.application.use_cases.generate_maintenance_plan import (
    GenerateMaintenancePlan,
)
from hermes.application.use_cases.generate_signal_maintenance_plan import (
    GenerateSignalMaintenancePlan,
)
from hermes.domain.maintenance import MaintenancePriority, StepKind
from hermes.infrastructure.maintenance.rule_based_maintenance_planner import (
    RuleBasedMaintenancePlanner,
)
from hermes.infrastructure.metrics.fake_metrics_reader import FakeMetricsReader
from hermes.infrastructure.operations.rule_based_operations_explainer import (
    RuleBasedOperationsExplainer,
)


class MaintenancePlanUseCasesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.metrics_reader = FakeMetricsReader()
        self.explainer = RuleBasedOperationsExplainer()
        self.planner = RuleBasedMaintenancePlanner()

    def test_generate_maintenance_plan_prioritizes_worker_queue(self) -> None:
        plan = GenerateMaintenancePlan(
            self.metrics_reader,
            self.explainer,
            self.planner,
        ).execute()

        self.assertEqual(plan.title, "Worker Queue Maintenance Plan")
        self.assertEqual(plan.priority, MaintenancePriority.MEDIUM)
        self.assertTrue(any(step.requires_approval for step in plan.steps))
        self.assertIn(StepKind.DOCUMENTATION, [step.kind for step in plan.steps])

    def test_generate_signal_maintenance_plan(self) -> None:
        plan = GenerateSignalMaintenancePlan(
            self.metrics_reader,
            self.explainer,
            self.planner,
        ).execute("worker_queue")

        self.assertEqual(plan.title, "Worker Queue Maintenance Plan")
        self.assertEqual(plan.steps[0].title, "Confirm worker health")

    def test_generate_signal_maintenance_plan_raises_when_missing(self) -> None:
        with self.assertRaises(OperationalSignalNotFound):
            GenerateSignalMaintenancePlan(
                self.metrics_reader,
                self.explainer,
                self.planner,
            ).execute("missing_signal")


if __name__ == "__main__":
    unittest.main()
