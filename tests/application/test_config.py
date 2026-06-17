import os
import unittest
from unittest.mock import patch

from hermes.config import (
    GrafanaSource,
    InvalidHermesConfig,
    load_config,
    parse_grafana_source,
)


class ConfigTest(unittest.TestCase):
    def test_defaults_to_safe_fake_grafana_source(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            config = load_config()

        self.assertEqual(config.grafana_source, GrafanaSource.FAKE_GRAFANA)

    def test_loads_fake_application_api_source(self) -> None:
        with patch.dict(
            os.environ,
            {"HERMES_GRAFANA_SOURCE": "fake_application_api"},
            clear=True,
        ):
            config = load_config()

        self.assertEqual(config.grafana_source, GrafanaSource.FAKE_APPLICATION_API)

    def test_rejects_unknown_grafana_source(self) -> None:
        with self.assertRaisesRegex(
            InvalidHermesConfig,
            "Invalid HERMES_GRAFANA_SOURCE",
        ):
            parse_grafana_source("direct_admin_access")

    def test_application_api_requires_base_url(self) -> None:
        with patch.dict(
            os.environ,
            {"HERMES_GRAFANA_SOURCE": "application_api"},
            clear=True,
        ):
            with self.assertRaisesRegex(
                InvalidHermesConfig,
                "HERMES_APPLICATION_API_BASE_URL is required",
            ):
                load_config()

    def test_application_api_accepts_base_url(self) -> None:
        with patch.dict(
            os.environ,
            {
                "HERMES_GRAFANA_SOURCE": "application_api",
                "HERMES_APPLICATION_API_BASE_URL": "http://app.local/",
            },
            clear=True,
        ):
            config = load_config()

        self.assertEqual(config.application_api_base_url, "http://app.local")


if __name__ == "__main__":
    unittest.main()
