import unittest

from hermes.config import GrafanaSource, HermesConfig
from hermes.infrastructure.application_api.fake_application_grafana_reader import (
    FakeApplicationGrafanaReader,
)
from hermes.infrastructure.application_api.application_api_grafana_reader import (
    ApplicationApiGrafanaReader,
)
from hermes.infrastructure.grafana.fake_grafana_reader import FakeGrafanaReader
from hermes.infrastructure.grafana_reader_factory import (
    UnknownGrafanaSource,
    create_grafana_reader,
)


class GrafanaReaderFactoryTest(unittest.TestCase):
    def test_creates_fake_grafana_reader_by_default(self) -> None:
        reader = create_grafana_reader(HermesConfig())

        self.assertIsInstance(reader, FakeGrafanaReader)

    def test_creates_fake_application_api_reader(self) -> None:
        reader = create_grafana_reader(
            HermesConfig(grafana_source=GrafanaSource.FAKE_APPLICATION_API)
        )

        self.assertIsInstance(reader, FakeApplicationGrafanaReader)

    def test_rejects_unknown_source(self) -> None:
        with self.assertRaises(UnknownGrafanaSource):
            create_grafana_reader(HermesConfig(grafana_source="unknown"))  # type: ignore[arg-type]

    def test_creates_application_api_reader(self) -> None:
        reader = create_grafana_reader(
            HermesConfig(
                grafana_source=GrafanaSource.APPLICATION_API,
                application_api_base_url="http://app.local",
            )
        )

        self.assertIsInstance(reader, ApplicationApiGrafanaReader)


if __name__ == "__main__":
    unittest.main()
