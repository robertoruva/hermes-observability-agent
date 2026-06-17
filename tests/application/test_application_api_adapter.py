import unittest

from hermes.application.use_cases.check_grafana_health import CheckGrafanaHealth
from hermes.application.use_cases.get_dashboard import GetDashboard
from hermes.application.use_cases.search_dashboards import SearchDashboards
from hermes.infrastructure.application_api.fake_application_grafana_reader import (
    FakeApplicationGrafanaReader,
)


class ApplicationApiAdapterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = FakeApplicationGrafanaReader()

    def test_use_cases_work_through_application_boundary(self) -> None:
        status = CheckGrafanaHealth(self.reader).execute()
        dashboards = SearchDashboards(self.reader).execute()
        dashboard = GetDashboard(self.reader).execute("app-admin-overview")

        self.assertEqual(status.service, "application-api")
        self.assertTrue(status.reachable)
        self.assertEqual(dashboards[0].uid, "app-admin-overview")
        self.assertIn("Admin health", dashboard.panels)


if __name__ == "__main__":
    unittest.main()
