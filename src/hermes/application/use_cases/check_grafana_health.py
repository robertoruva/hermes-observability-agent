from hermes.domain.health import HealthStatus
from hermes.ports.grafana_reader import GrafanaReader


class CheckGrafanaHealth:
    def __init__(self, grafana_reader: GrafanaReader) -> None:
        self._grafana_reader = grafana_reader

    def execute(self) -> HealthStatus:
        return self._grafana_reader.check_health()
