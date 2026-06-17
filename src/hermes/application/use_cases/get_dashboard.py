from hermes.domain.dashboard import Dashboard
from hermes.ports.grafana_reader import GrafanaReader


class GetDashboard:
    def __init__(self, grafana_reader: GrafanaReader) -> None:
        self._grafana_reader = grafana_reader

    def execute(self, uid: str) -> Dashboard:
        return self._grafana_reader.get_dashboard(uid)
