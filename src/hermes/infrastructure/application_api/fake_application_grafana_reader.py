from hermes.domain.dashboard import Dashboard, DashboardSummary
from hermes.domain.errors import DashboardNotFound
from hermes.domain.health import HealthStatus


class FakeApplicationGrafanaReader:
    """Demo adapter for reading Grafana data through an existing application API.

    This represents the preferred private shape:
    Hermes talks to the application boundary, and the application owns the
    real permissions, validation, and infrastructure access.
    """

    def __init__(self) -> None:
        self._dashboards = {
            "app-admin-overview": Dashboard(
                uid="app-admin-overview",
                title="Application Admin Overview",
                panels=("Admin health", "Background jobs", "Integration status"),
            ),
            "app-operations": Dashboard(
                uid="app-operations",
                title="Application Operations",
                panels=("Request volume", "Error budget", "Queue depth"),
            ),
        }

    def check_health(self) -> HealthStatus:
        return HealthStatus(
            service="application-api",
            reachable=True,
            message="Fake application API boundary is available.",
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
