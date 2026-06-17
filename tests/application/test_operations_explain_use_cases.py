import unittest

from hermes.application.use_cases.explain_metrics_snapshot import ExplainMetricsSnapshot
from hermes.application.use_cases.explain_operational_signal import (
    ExplainOperationalSignal,
    OperationalSignalNotFound,
)
from hermes.domain.operations import ExplanationConfidence
from hermes.infrastructure.metrics.fake_metrics_reader import FakeMetricsReader
from hermes.infrastructure.operations.rule_based_operations_explainer import (
    RuleBasedOperationsExplainer,
)


class OperationsExplainUseCasesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.metrics_reader = FakeMetricsReader()
        self.explainer = RuleBasedOperationsExplainer()

    def test_explain_metrics_snapshot(self) -> None:
        explanations = ExplainMetricsSnapshot(
            self.metrics_reader,
            self.explainer,
        ).execute()

        self.assertGreaterEqual(len(explanations), 4)
        self.assertEqual(explanations[0].signal, "database")
        self.assertEqual(explanations[0].confidence, ExplanationConfidence.HIGH)

    def test_explain_worker_queue_signal(self) -> None:
        explanation = ExplainOperationalSignal(
            self.metrics_reader,
            self.explainer,
        ).execute("worker_queue")

        self.assertEqual(explanation.signal, "worker_queue")
        self.assertIn("Jobs are waiting", explanation.meaning)
        self.assertIn("check worker health", explanation.recommended_checks)
        self.assertIn("restart production automatically", explanation.unsafe_actions)

    def test_explain_missing_signal_raises(self) -> None:
        with self.assertRaises(OperationalSignalNotFound):
            ExplainOperationalSignal(
                self.metrics_reader,
                self.explainer,
            ).execute("missing_signal")


if __name__ == "__main__":
    unittest.main()
