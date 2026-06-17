from hermes.domain.dashboard import DashboardSummary
from hermes.ports.grafana_reader import GrafanaReader


class SearchDashboards:
    def __init__(self, grafana_reader: GrafanaReader) -> None:
        self._grafana_reader = grafana_reader

    def execute(self) -> list[DashboardSummary]:
        return self._grafana_reader.search_dashboards()
