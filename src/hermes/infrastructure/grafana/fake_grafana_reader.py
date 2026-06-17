from hermes.domain.dashboard import Dashboard, DashboardSummary
from hermes.domain.errors import DashboardNotFound
from hermes.domain.health import HealthStatus


class FakeGrafanaReader:
    """Demo adapter used before connecting Hermes to real Grafana."""

    def __init__(self) -> None:
        self._dashboards = {
            "demo-system-overview": Dashboard(
                uid="demo-system-overview",
                title="Demo System Overview",
                panels=("API latency", "Worker health", "Error rate"),
            ),
            "demo-api-latency": Dashboard(
                uid="demo-api-latency",
                title="Demo API Latency",
                panels=("p50 latency", "p95 latency", "p99 latency"),
            ),
        }

    def check_health(self) -> HealthStatus:
        return HealthStatus(
            service="grafana",
            reachable=True,
            message="Fake Grafana reader is available.",
        )

    def search_dashboards(self) -> list[DashboardSummary]:
        return [
            DashboardSummary(uid=dashboard.uid, title=dashboard.title)
            for dashboard in self._dashboards.values()
        ]

    def get_dashboard(self, uid: str) -> Dashboard:
        try:
            return self._dashboards[uid]
        except KeyError as exc:
            raise DashboardNotFound(uid) from exc
