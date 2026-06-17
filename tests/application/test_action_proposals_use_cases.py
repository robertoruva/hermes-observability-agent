import unittest

from hermes.application.use_cases.explain_operational_signal import (
    OperationalSignalNotFound,
)
from hermes.application.use_cases.propose_maintenance_actions import (
    ProposeMaintenanceActions,
)
from hermes.application.use_cases.propose_signal_actions import ProposeSignalActions
from hermes.domain.actions import ProposalRisk, ProposalType
from hermes.infrastructure.actions.rule_based_action_proposer import (
    RuleBasedActionProposer,
)
from hermes.infrastructure.maintenance.rule_based_maintenance_planner import (
    RuleBasedMaintenancePlanner,
)
from hermes.infrastructure.metrics.fake_metrics_reader import FakeMetricsReader
from hermes.infrastructure.operations.rule_based_operations_explainer import (
    RuleBasedOperationsExplainer,
)


class ActionProposalsUseCasesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.metrics_reader = FakeMetricsReader()
        self.explainer = RuleBasedOperationsExplainer()
        self.planner = RuleBasedMaintenancePlanner()
        self.proposer = RuleBasedActionProposer()

    def test_propose_maintenance_actions_returns_reviewable_proposals(self) -> None:
        proposals = ProposeMaintenanceActions(
            self.metrics_reader,
            self.explainer,
            self.planner,
            self.proposer,
        ).execute()

        capacity_review = proposals[0]
        self.assertEqual(capacity_review.title, "Review worker capacity")
        self.assertEqual(capacity_review.proposal_type, ProposalType.CAPACITY_REVIEW)
        self.assertEqual(capacity_review.risk, ProposalRisk.MEDIUM)
        self.assertTrue(capacity_review.approval_required)
        self.assertIn("worker_queue trend is increasing", capacity_review.evidence)
        self.assertIn(
            "do not change scaling automatically",
            capacity_review.must_not_execute,
        )

    def test_propose_signal_actions_returns_signal_specific_proposals(self) -> None:
        proposals = ProposeSignalActions(
            self.metrics_reader,
            self.explainer,
            self.planner,
            self.proposer,
        ).execute("api_latency")

        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0].proposal_type, ProposalType.THRESHOLD_REVIEW)
        self.assertFalse(proposals[0].approval_required)

    def test_propose_signal_actions_raises_when_missing(self) -> None:
        with self.assertRaises(OperationalSignalNotFound):
            ProposeSignalActions(
                self.metrics_reader,
                self.explainer,
                self.planner,
                self.proposer,
            ).execute("missing_signal")


if __name__ == "__main__":
    unittest.main()
