import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from hermes.domain.dashboard import Dashboard, DashboardSummary
from hermes.domain.errors import DashboardNotFound
from hermes.domain.health import HealthStatus
from hermes.infrastructure.application_api.contract import (
    GRAFANA_HEALTH_PATH,
    GRAFANA_SEARCH_PATH,
    grafana_dashboard_path,
)


@dataclass(frozen=True)
class ApplicationApiSettings:
    base_url: str
    timeout_seconds: float = 2.0


class ApplicationApiGrafanaReader:
    """Read Grafana-shaped data through the existing application API."""

    def __init__(self, settings: ApplicationApiSettings) -> None:
        self._settings = settings

    def check_health(self) -> HealthStatus:
        payload = self._get_json(GRAFANA_HEALTH_PATH)
        return HealthStatus(
            service=str(payload.get("service", "application-api")),
            reachable=bool(payload.get("reachable", False)),
            message=str(payload.get("message", "")),
        )

    def search_dashboards(self) -> list[DashboardSummary]:
        payload = self._get_json(GRAFANA_SEARCH_PATH)
        if not isinstance(payload, list):
            raise ApplicationApiError("Expected dashboard search response to be a list.")

        return [
            DashboardSummary(
                uid=str(item["uid"]),
                title=str(item["title"]),
                url=item.get("url"),
            )
            for item in payload
        ]

    def get_dashboard(self, uid: str) -> Dashboard:
        try:
            payload = self._get_json(grafana_dashboard_path(uid))
        except ApplicationApiNotFound as exc:
            raise DashboardNotFound(uid) from exc

        panels = payload.get("panels", ())
        if not isinstance(panels, list):
            raise ApplicationApiError("Expected dashboard panels to be a list.")

        return Dashboard(
            uid=str(payload["uid"]),
            title=str(payload["title"]),
            panels=tuple(str(panel) for panel in panels),
        )

    def _get_json(self, path: str) -> Any:
        url = f"{self._settings.base_url}{path}"
        request = Request(url, headers={"Accept": "application/json"}, method="GET")

        try:
            with urlopen(request, timeout=self._settings.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code == 404:
                raise ApplicationApiNotFound(path) from exc
            raise ApplicationApiError(f"Application API returned HTTP {exc.code}.") from exc
        except URLError as exc:
            raise ApplicationApiError(f"Application API is unreachable: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise ApplicationApiError("Application API returned invalid JSON.") from exc


class ApplicationApiError(Exception):
    pass


class ApplicationApiNotFound(ApplicationApiError):
    def __init__(self, path: str) -> None:
        super().__init__(f"Application API resource not found: {path}")
        self.path = path
