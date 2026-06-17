from hermes.domain.actions import ActionProposal, ProposalRisk, ProposalType
from hermes.domain.maintenance import MaintenancePlan, StepKind


class RuleBasedActionProposer:
    """Public-safe deterministic proposals for advisory maintenance plans."""

    def propose_actions(self, plan: MaintenancePlan) -> list[ActionProposal]:
        if plan.title == "Worker Queue Maintenance Plan":
            return self._worker_queue_proposals()

        if plan.title == "Database Signal Maintenance Plan":
            return self._database_proposals()

        if plan.title == "API Latency Maintenance Plan":
            return self._api_latency_proposals()

        if plan.title == "Scrape Targets Maintenance Plan":
            return self._scrape_target_proposals()

        return self._general_proposals(plan)

    def _worker_queue_proposals(self) -> list[ActionProposal]:
        return [
            ActionProposal(
                title="Review worker capacity",
                proposal_type=ProposalType.CAPACITY_REVIEW,
                reason=(
                    "The worker queue is degraded and increasing, so background "
                    "work may become delayed if the trend continues."
                ),
                evidence=(
                    "worker_queue status is degraded",
                    "worker_queue trend is increasing",
                    "maintenance plan includes a capacity recommendation",
                ),
                preconditions=(
                    "confirm workers are healthy",
                    "check for repeated job failures",
                    "confirm the queue trend persists",
                ),
                approval_required=True,
                risk=ProposalRisk.MEDIUM,
                human_action=(
                    "Open an operational review and decide whether worker "
                    "capacity should be adjusted."
                ),
                must_not_execute=(
                    "do not restart workers automatically",
                    "do not change scaling automatically",
                    "do not delete queued messages",
                ),
            ),
            ActionProposal(
                title="Document queue review threshold",
                proposal_type=ProposalType.RUNBOOK_DOCUMENTATION,
                reason=(
                    "The plan includes documentation because queue growth should "
                    "have an explicit review threshold."
                ),
                evidence=(
                    "maintenance plan includes documentation",
                    "queue growth is the selected synthetic scenario",
                ),
                preconditions=(
                    "agree on the queue depth or trend that should trigger review",
                    "confirm where the runbook should live",
                ),
                approval_required=False,
                risk=ProposalRisk.LOW,
                human_action=(
                    "Document when queue growth should be investigated and who "
                    "owns the follow-up."
                ),
                must_not_execute=(
                    "do not treat documentation as remediation",
                    "do not hide approval requirements for capacity changes",
                ),
            ),
        ]

    def _database_proposals(self) -> list[ActionProposal]:
        return [
            ActionProposal(
                title="Document database health boundary",
                proposal_type=ProposalType.RUNBOOK_DOCUMENTATION,
                reason=(
                    "Database reachability is healthy, but reachability does not "
                    "prove query performance."
                ),
                evidence=(
                    "database signal is healthy",
                    "maintenance plan separates connectivity from performance",
                ),
                preconditions=(
                    "confirm which checks are available in the private environment",
                    "confirm where database performance notes should be documented",
                ),
                approval_required=False,
                risk=ProposalRisk.LOW,
                human_action=(
                    "Document what the database signal proves and which extra "
                    "signals are needed for performance."
                ),
                must_not_execute=(
                    "do not change database configuration from Hermes",
                    "do not assume all database queries are fast",
                ),
            )
        ]

    def _api_latency_proposals(self) -> list[ActionProposal]:
        return [
            ActionProposal(
                title="Review API latency thresholds",
                proposal_type=ProposalType.THRESHOLD_REVIEW,
                reason=(
                    "API latency is stable in the demo, so the useful action is "
                    "to keep review thresholds explicit."
                ),
                evidence=(
                    "api_latency signal is stable",
                    "maintenance plan recommends comparing percentiles",
                ),
                preconditions=(
                    "define which endpoints are user-facing",
                    "compare p50, p95, and p99 in private monitoring",
                ),
                approval_required=False,
                risk=ProposalRisk.LOW,
                human_action=(
                    "Review whether API latency warning thresholds are clear and "
                    "visible."
                ),
                must_not_execute=(
                    "do not assume one average represents every endpoint",
                    "do not change alerting rules automatically",
                ),
            )
        ]

    def _scrape_target_proposals(self) -> list[ActionProposal]:
        return [
            ActionProposal(
                title="Review dashboard coverage",
                proposal_type=ProposalType.DASHBOARD_COVERAGE_REVIEW,
                reason=(
                    "Reachable scrape targets mean metrics can be collected, but "
                    "they do not prove all important behavior is visible."
                ),
                evidence=(
                    "scrape_targets signal is healthy",
                    "maintenance plan asks to check dashboard gaps",
                ),
                preconditions=(
                    "list critical service behaviors",
                    "compare service behaviors with visible dashboards",
                ),
                approval_required=False,
                risk=ProposalRisk.LOW,
                human_action=(
                    "Review whether dashboards cover the operational behavior "
                    "the team cares about."
                ),
                must_not_execute=(
                    "do not edit dashboards automatically",
                    "do not assume scrape success means the feature is healthy",
                ),
            )
        ]

    def _general_proposals(self, plan: MaintenancePlan) -> list[ActionProposal]:
        approval_required = any(step.requires_approval for step in plan.steps)
        proposal_steps = [
            step.title for step in plan.steps if step.kind == StepKind.PROPOSAL
        ]
        evidence = tuple(proposal_steps) or ("maintenance plan exists",)

        return [
            ActionProposal(
                title="Review maintenance plan",
                proposal_type=ProposalType.GENERAL_REVIEW,
                reason="The maintenance plan should be reviewed before action.",
                evidence=evidence,
                preconditions=(
                    "confirm the plan is based on current operational signals",
                    "confirm the owning human reviewer",
                ),
                approval_required=approval_required,
                risk=ProposalRisk.MEDIUM if approval_required else ProposalRisk.LOW,
                human_action="Review the plan and decide which steps are worth doing.",
                must_not_execute=(
                    "do not execute infrastructure changes automatically",
                    "do not skip human review",
                ),
            )
        ]
