import unittest

from hermes.application.use_cases.check_grafana_health import CheckGrafanaHealth
from hermes.application.use_cases.get_dashboard import GetDashboard
from hermes.application.use_cases.search_dashboards import SearchDashboards
from hermes.infrastructure.grafana.fake_grafana_reader import (
    DashboardNotFound,
    FakeGrafanaReader,
)


class GrafanaUseCasesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = FakeGrafanaReader()

    def test_check_grafana_health(self) -> None:
        status = CheckGrafanaHealth(self.reader).execute()

        self.assertEqual(status.service, "grafana")
        self.assertTrue(status.reachable)

    def test_search_dashboards(self) -> None:
        dashboards = SearchDashboards(self.reader).execute()

        self.assertGreaterEqual(len(dashboards), 2)
        self.assertEqual(dashboards[0].uid, "demo-system-overview")

    def test_get_dashboard(self) -> None:
        dashboard = GetDashboard(self.reader).execute("demo-system-overview")

        self.assertEqual(dashboard.title, "Demo System Overview")
        self.assertIn("API latency", dashboard.panels)

    def test_get_dashboard_raises_when_missing(self) -> None:
        with self.assertRaises(DashboardNotFound):
            GetDashboard(self.reader).execute("missing-dashboard")


if __name__ == "__main__":
    unittest.main()
