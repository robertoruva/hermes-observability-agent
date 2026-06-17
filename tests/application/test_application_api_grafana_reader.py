import json
import unittest
from urllib.error import HTTPError
from unittest.mock import patch

from hermes.domain.errors import DashboardNotFound
from hermes.infrastructure.application_api.application_api_grafana_reader import (
    ApplicationApiGrafanaReader,
    ApplicationApiSettings,
)


class FakeHttpResponse:
    def __init__(self, payload: object) -> None:
        self._payload = payload

    def __enter__(self) -> "FakeHttpResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


class FakeHttpError(HTTPError):
    def __init__(self, code: int) -> None:
        Exception.__init__(self, "Fake HTTP error")
        self.code = code


class ApplicationApiGrafanaReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = ApplicationApiGrafanaReader(
            ApplicationApiSettings(base_url="http://app.local")
        )

    @patch("hermes.infrastructure.application_api.application_api_grafana_reader.urlopen")
    def test_check_health(self, urlopen_mock) -> None:
        urlopen_mock.return_value = FakeHttpResponse(
            {
                "service": "application-api",
                "reachable": True,
                "message": "ok",
            }
        )

        status = self.reader.check_health()

        self.assertEqual(status.service, "application-api")
        self.assertTrue(status.reachable)
        request = urlopen_mock.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "http://app.local/internal/hermes/grafana/health",
        )

    @patch("hermes.infrastructure.application_api.application_api_grafana_reader.urlopen")
    def test_search_dashboards(self, urlopen_mock) -> None:
        urlopen_mock.return_value = FakeHttpResponse(
            [{"uid": "admin", "title": "Admin", "url": "/d/admin"}]
        )

        dashboards = self.reader.search_dashboards()

        self.assertEqual(dashboards[0].uid, "admin")
        self.assertEqual(dashboards[0].title, "Admin")
        request = urlopen_mock.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "http://app.local/internal/hermes/grafana/search",
        )

    @patch("hermes.infrastructure.application_api.application_api_grafana_reader.urlopen")
    def test_get_dashboard(self, urlopen_mock) -> None:
        urlopen_mock.return_value = FakeHttpResponse(
            {"uid": "admin", "title": "Admin", "panels": ["Health"]}
        )

        dashboard = self.reader.get_dashboard("admin")

        self.assertEqual(dashboard.uid, "admin")
        self.assertEqual(dashboard.panels, ("Health",))
        request = urlopen_mock.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "http://app.local/internal/hermes/grafana/dashboards/admin",
        )

    @patch("hermes.infrastructure.application_api.application_api_grafana_reader.urlopen")
    def test_get_dashboard_url_encodes_uid(self, urlopen_mock) -> None:
        urlopen_mock.return_value = FakeHttpResponse(
            {"uid": "team/a b", "title": "Team", "panels": []}
        )

        self.reader.get_dashboard("team/a b")

        request = urlopen_mock.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "http://app.local/internal/hermes/grafana/dashboards/team%2Fa%20b",
        )

    @patch("hermes.infrastructure.application_api.application_api_grafana_reader.urlopen")
    def test_get_dashboard_maps_404_to_domain_error(self, urlopen_mock) -> None:
        urlopen_mock.side_effect = FakeHttpError(404)

        with self.assertRaises(DashboardNotFound):
            self.reader.get_dashboard("missing")


if __name__ == "__main__":
    unittest.main()
