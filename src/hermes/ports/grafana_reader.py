from typing import Protocol

from hermes.domain.dashboard import Dashboard, DashboardSummary
from hermes.domain.health import HealthStatus


class GrafanaReader(Protocol):
    """Read-only port for Grafana-like dashboard providers."""

    def check_health(self) -> HealthStatus:
        """Return whether the Grafana provider is reachable."""

    def search_dashboards(self) -> list[DashboardSummary]:
        """Return dashboards visible to the configured read-only identity."""

    def get_dashboard(self, uid: str) -> Dashboard:
        """Return one dashboard by UID."""
