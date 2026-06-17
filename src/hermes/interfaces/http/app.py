import os

from fastapi import FastAPI, HTTPException

from hermes.application.use_cases.propose_maintenance_actions import (
    ProposeMaintenanceActions,
)
from hermes.application.use_cases.propose_signal_actions import ProposeSignalActions
from hermes.application.use_cases.check_grafana_health import CheckGrafanaHealth
from hermes.application.use_cases.explain_metrics_snapshot import ExplainMetricsSnapshot
from hermes.application.use_cases.explain_operational_signal import (
    ExplainOperationalSignal,
    OperationalSignalNotFound,
)
from hermes.application.use_cases.generate_maintenance_plan import (
    GenerateMaintenancePlan,
)
from hermes.application.use_cases.generate_signal_maintenance_plan import (
    GenerateSignalMaintenancePlan,
)
from hermes.application.use_cases.get_dashboard import GetDashboard
from hermes.application.use_cases.list_operational_signals import ListOperationalSignals
from hermes.application.use_cases.read_metrics_snapshot import ReadMetricsSnapshot
from hermes.application.use_cases.search_dashboards import SearchDashboards
from hermes.config import load_config
from hermes.domain.actions import ActionProposal
from hermes.domain.errors import DashboardNotFound
from hermes.domain.maintenance import MaintenancePlan, MaintenanceStep
from hermes.domain.metrics import MetricsSnapshot, OperationalSignal
from hermes.domain.operations import OperationalExplanation
from hermes.infrastructure.action_proposer_factory import create_action_proposer
from hermes.infrastructure.grafana_reader_factory import create_grafana_reader
from hermes.infrastructure.maintenance_planner_factory import (
    create_maintenance_planner,
)
from hermes.infrastructure.metrics_reader_factory import create_metrics_reader
from hermes.infrastructure.operations_explainer_factory import (
    create_operations_explainer,
)


def ensure_container_runtime() -> None:
    if os.getenv("HERMES_CONTAINER_RUNTIME") != "docker":
        raise RuntimeError(
            "Hermes Observability Agent is designed to run through its Docker workflow. "
            "Use docker compose -f docker-compose.demo.yml up --build."
        )


def create_app() -> FastAPI:
    ensure_container_runtime()

    app = FastAPI(
        title="Hermes Observability Agent",
        description="A bounded read-only observability agent.",
        version="0.1.0",
    )
    config = load_config()
    grafana_reader = create_grafana_reader(config)
    metrics_reader = create_metrics_reader()
    operations_explainer = create_operations_explainer()
    maintenance_planner = create_maintenance_planner()
    action_proposer = create_action_proposer()

    @app.get("/health")
    def health() -> dict[str, object]:
        status = CheckGrafanaHealth(grafana_reader).execute()
        return {
            "service": status.service,
            "reachable": status.reachable,
            "message": status.message,
            "source": config.grafana_source.value,
        }

    @app.get("/api/grafana/search")
    def search_dashboards() -> list[dict[str, str | None]]:
        dashboards = SearchDashboards(grafana_reader).execute()
        return [
            {"uid": dashboard.uid, "title": dashboard.title, "url": dashboard.url}
            for dashboard in dashboards
        ]

    @app.get("/api/grafana/dashboards/{uid}")
    def get_dashboard(uid: str) -> dict[str, object]:
        try:
            dashboard = GetDashboard(grafana_reader).execute(uid)
        except DashboardNotFound as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return {
            "uid": dashboard.uid,
            "title": dashboard.title,
            "panels": list(dashboard.panels),
        }

    @app.get("/api/metrics/summary")
    def metrics_summary() -> dict[str, object]:
        snapshot = ReadMetricsSnapshot(metrics_reader).execute()
        return serialize_metrics_snapshot(snapshot)

    @app.get("/api/metrics/signals")
    def metrics_signals() -> list[dict[str, str]]:
        signals = ListOperationalSignals(metrics_reader).execute()
        return [serialize_operational_signal(signal) for signal in signals]

    @app.get("/api/operations/explanations")
    def operations_explanations() -> list[dict[str, object]]:
        explanations = ExplainMetricsSnapshot(
            metrics_reader,
            operations_explainer,
        ).execute()
        return [
            serialize_operational_explanation(explanation)
            for explanation in explanations
        ]

    @app.get("/api/operations/explanations/{signal_name}")
    def operation_explanation(signal_name: str) -> dict[str, object]:
        try:
            explanation = ExplainOperationalSignal(
                metrics_reader,
                operations_explainer,
            ).execute(signal_name)
        except OperationalSignalNotFound as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return serialize_operational_explanation(explanation)

    @app.get("/api/maintenance/plan")
    def maintenance_plan() -> dict[str, object]:
        plan = GenerateMaintenancePlan(
            metrics_reader,
            operations_explainer,
            maintenance_planner,
        ).execute()
        return serialize_maintenance_plan(plan)

    @app.get("/api/maintenance/plan/{signal_name}")
    def signal_maintenance_plan(signal_name: str) -> dict[str, object]:
        try:
            plan = GenerateSignalMaintenancePlan(
                metrics_reader,
                operations_explainer,
                maintenance_planner,
            ).execute(signal_name)
        except OperationalSignalNotFound as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return serialize_maintenance_plan(plan)

    @app.get("/api/actions/proposals")
    def action_proposals() -> list[dict[str, object]]:
        proposals = ProposeMaintenanceActions(
            metrics_reader,
            operations_explainer,
            maintenance_planner,
            action_proposer,
        ).execute()
        return [serialize_action_proposal(proposal) for proposal in proposals]

    @app.get("/api/actions/proposals/{signal_name}")
    def signal_action_proposals(signal_name: str) -> list[dict[str, object]]:
        try:
            proposals = ProposeSignalActions(
                metrics_reader,
                operations_explainer,
                maintenance_planner,
                action_proposer,
            ).execute(signal_name)
        except OperationalSignalNotFound as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        return [serialize_action_proposal(proposal) for proposal in proposals]

    return app


def serialize_metrics_snapshot(snapshot: MetricsSnapshot) -> dict[str, object]:
    return {
        "source": snapshot.source,
        "signals": [
            serialize_operational_signal(signal) for signal in snapshot.signals
        ],
    }


def serialize_operational_signal(signal: OperationalSignal) -> dict[str, str]:
    return {
        "name": signal.name,
        "status": signal.status.value,
        "severity": signal.severity.value,
        "summary": signal.summary,
        "trend": signal.trend.value,
    }


def serialize_operational_explanation(
    explanation: OperationalExplanation,
) -> dict[str, object]:
    return {
        "signal": explanation.signal,
        "meaning": explanation.meaning,
        "risk": explanation.risk,
        "possible_causes": list(explanation.possible_causes),
        "recommended_checks": list(explanation.recommended_checks),
        "safe_actions": list(explanation.safe_actions),
        "unsafe_actions": list(explanation.unsafe_actions),
        "confidence": explanation.confidence.value,
    }


def serialize_maintenance_plan(plan: MaintenancePlan) -> dict[str, object]:
    return {
        "title": plan.title,
        "priority": plan.priority.value,
        "summary": plan.summary,
        "steps": [serialize_maintenance_step(step) for step in plan.steps],
    }


def serialize_maintenance_step(step: MaintenanceStep) -> dict[str, object]:
    return {
        "order": step.order,
        "title": step.title,
        "kind": step.kind.value,
        "risk": step.risk.value,
        "requires_approval": step.requires_approval,
        "summary": step.summary,
    }


def serialize_action_proposal(proposal: ActionProposal) -> dict[str, object]:
    return {
        "title": proposal.title,
        "proposal_type": proposal.proposal_type.value,
        "reason": proposal.reason,
        "evidence": list(proposal.evidence),
        "preconditions": list(proposal.preconditions),
        "approval_required": proposal.approval_required,
        "risk": proposal.risk.value,
        "human_action": proposal.human_action,
        "must_not_execute": list(proposal.must_not_execute),
    }


app = create_app()
