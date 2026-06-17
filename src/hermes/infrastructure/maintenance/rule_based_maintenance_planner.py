from hermes.domain.maintenance import (
    MaintenancePlan,
    MaintenancePriority,
    MaintenanceStep,
    StepKind,
    StepRisk,
)
from hermes.domain.operations import OperationalExplanation


class RuleBasedMaintenancePlanner:
    """Public-safe deterministic planner for synthetic explanations."""

    def generate_plan(
        self,
        explanations: list[OperationalExplanation],
    ) -> MaintenancePlan:
        if any(explanation.signal == "worker_queue" for explanation in explanations):
            return self._worker_queue_plan()

        if len(explanations) == 1:
            explanation = explanations[0]
            if explanation.signal == "database":
                return self._database_plan()
            if explanation.signal == "api_latency":
                return self._api_latency_plan()
            if explanation.signal == "scrape_targets":
                return self._scrape_targets_plan()

        return self._general_plan()

    def _worker_queue_plan(self) -> MaintenancePlan:
        return MaintenancePlan(
            title="Worker Queue Maintenance Plan",
            priority=MaintenancePriority.MEDIUM,
            summary=(
                "Queue growth should be reviewed before delayed background work "
                "starts affecting users."
            ),
            steps=(
                MaintenanceStep(
                    order=1,
                    title="Confirm worker health",
                    kind=StepKind.CHECK,
                    risk=StepRisk.LOW,
                    requires_approval=False,
                    summary=(
                        "Verify that the expected workers are alive through the "
                        "approved application boundary."
                    ),
                ),
                MaintenanceStep(
                    order=2,
                    title="Review repeated job failures",
                    kind=StepKind.INVESTIGATION,
                    risk=StepRisk.LOW,
                    requires_approval=False,
                    summary=(
                        "Look for repeated failures or retries that could explain "
                        "why the queue is growing."
                    ),
                ),
                MaintenanceStep(
                    order=3,
                    title="Document queue observation and thresholds",
                    kind=StepKind.DOCUMENTATION,
                    risk=StepRisk.LOW,
                    requires_approval=False,
                    summary=(
                        "Record what the queue signal proves, what it does not "
                        "prove, and which thresholds should trigger review."
                    ),
                ),
                MaintenanceStep(
                    order=4,
                    title="Prepare capacity recommendation",
                    kind=StepKind.PROPOSAL,
                    risk=StepRisk.MEDIUM,
                    requires_approval=True,
                    summary=(
                        "Prepare a human-reviewed proposal before changing worker "
                        "capacity or infrastructure."
                    ),
                ),
            ),
        )

    def _database_plan(self) -> MaintenancePlan:
        return MaintenancePlan(
            title="Database Signal Maintenance Plan",
            priority=MaintenancePriority.LOW,
            summary=(
                "Database reachability is healthy in the synthetic demo, but it "
                "should remain separate from query performance."
            ),
            steps=(
                MaintenanceStep(
                    order=1,
                    title="Document database health boundary",
                    kind=StepKind.DOCUMENTATION,
                    risk=StepRisk.LOW,
                    requires_approval=False,
                    summary=(
                        "Write down that the signal proves connectivity, not full "
                        "query performance."
                    ),
                ),
                MaintenanceStep(
                    order=2,
                    title="Review latency and query errors separately",
                    kind=StepKind.CHECK,
                    risk=StepRisk.LOW,
                    requires_approval=False,
                    summary=(
                        "Keep database latency, query errors, and connection pool "
                        "health as separate private checks."
                    ),
                ),
            ),
        )

    def _api_latency_plan(self) -> MaintenancePlan:
        return MaintenancePlan(
            title="API Latency Maintenance Plan",
            priority=MaintenancePriority.LOW,
            summary=(
                "API latency is stable in the synthetic demo, so the maintenance "
                "focus is keeping useful thresholds visible."
            ),
            steps=(
                MaintenanceStep(
                    order=1,
                    title="Compare latency percentiles",
                    kind=StepKind.CHECK,
                    risk=StepRisk.LOW,
                    requires_approval=False,
                    summary=(
                        "Review p50, p95, and p99 separately instead of trusting a "
                        "single average."
                    ),
                ),
                MaintenanceStep(
                    order=2,
                    title="Define warning thresholds",
                    kind=StepKind.DOCUMENTATION,
                    risk=StepRisk.LOW,
                    requires_approval=False,
                    summary=(
                        "Document which latency thresholds should lead to a warning "
                        "or maintenance review."
                    ),
                ),
            ),
        )

    def _scrape_targets_plan(self) -> MaintenancePlan:
        return MaintenancePlan(
            title="Scrape Targets Maintenance Plan",
            priority=MaintenancePriority.LOW,
            summary=(
                "Scrape targets are reachable in the synthetic demo, so the next "
                "step is documenting what each target actually represents."
            ),
            steps=(
                MaintenanceStep(
                    order=1,
                    title="Map targets to service behavior",
                    kind=StepKind.DOCUMENTATION,
                    risk=StepRisk.LOW,
                    requires_approval=False,
                    summary=(
                        "Document which service behavior each scrape target helps "
                        "observe."
                    ),
                ),
                MaintenanceStep(
                    order=2,
                    title="Check for dashboard gaps",
                    kind=StepKind.CHECK,
                    risk=StepRisk.LOW,
                    requires_approval=False,
                    summary=(
                        "Review whether important service behavior is missing from "
                        "the dashboards."
                    ),
                ),
            ),
        )

    def _general_plan(self) -> MaintenancePlan:
        return MaintenancePlan(
            title="General Observability Maintenance Plan",
            priority=MaintenancePriority.LOW,
            summary=(
                "Synthetic operational signals should be reviewed, documented, "
                "and kept separate from automatic remediation."
            ),
            steps=(
                MaintenanceStep(
                    order=1,
                    title="Review explained signals",
                    kind=StepKind.CHECK,
                    risk=StepRisk.LOW,
                    requires_approval=False,
                    summary=(
                        "Read each explanation and confirm which signals need "
                        "follow-up."
                    ),
                ),
                MaintenanceStep(
                    order=2,
                    title="Document signal ownership",
                    kind=StepKind.DOCUMENTATION,
                    risk=StepRisk.LOW,
                    requires_approval=False,
                    summary=(
                        "Record who owns each signal and what operational question "
                        "it answers."
                    ),
                ),
                MaintenanceStep(
                    order=3,
                    title="Prepare reviewed improvement proposals",
                    kind=StepKind.PROPOSAL,
                    risk=StepRisk.MEDIUM,
                    requires_approval=True,
                    summary=(
                        "Any infrastructure or configuration improvement should be "
                        "prepared as a proposal before execution."
                    ),
                ),
            ),
        )
