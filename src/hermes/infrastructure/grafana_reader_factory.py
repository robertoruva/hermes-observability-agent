from hermes.config import GrafanaSource, HermesConfig
from hermes.infrastructure.application_api.application_api_grafana_reader import (
    ApplicationApiGrafanaReader,
    ApplicationApiSettings,
)
from hermes.infrastructure.application_api.fake_application_grafana_reader import (
    FakeApplicationGrafanaReader,
)
from hermes.infrastructure.grafana.fake_grafana_reader import FakeGrafanaReader
from hermes.ports.grafana_reader import GrafanaReader


def create_grafana_reader(config: HermesConfig) -> GrafanaReader:
    if config.grafana_source == GrafanaSource.FAKE_GRAFANA:
        return FakeGrafanaReader()

    if config.grafana_source == GrafanaSource.FAKE_APPLICATION_API:
        return FakeApplicationGrafanaReader()

    if config.grafana_source == GrafanaSource.APPLICATION_API:
        if config.application_api_base_url is None:
            raise UnknownGrafanaSource(config.grafana_source)
        return ApplicationApiGrafanaReader(
            ApplicationApiSettings(
                base_url=config.application_api_base_url,
                timeout_seconds=config.application_api_timeout_seconds,
            )
        )

    raise UnknownGrafanaSource(config.grafana_source)


class UnknownGrafanaSource(ValueError):
    def __init__(self, source: GrafanaSource) -> None:
        super().__init__(f"Unknown Grafana source: {source}")
        self.source = source
