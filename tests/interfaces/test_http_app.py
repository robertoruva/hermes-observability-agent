import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from hermes.interfaces.http.app import create_app


class HttpAppTest(unittest.TestCase):
    def create_client(self, env: dict[str, str] | None = None) -> TestClient:
        runtime_env = {"HERMES_CONTAINER_RUNTIME": "docker"}
        runtime_env.update(env or {})
        with patch.dict(os.environ, runtime_env, clear=True):
            return TestClient(create_app())

    def test_app_requires_docker_runtime(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "Docker workflow"):
                create_app()

    def test_health_returns_configured_source(self) -> None:
        client = self.create_client()

        response = client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "service": "grafana",
                "reachable": True,
                "message": "Fake Grafana reader is available.",
                "source": "fake_grafana",
            },
        )

    def test_search_dashboards_returns_public_demo_data(self) -> None:
        client = self.create_client()

        response = client.get("/api/grafana/search")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "uid": "demo-system-overview",
                    "title": "Demo System Overview",
                    "url": None,
                },
                {
                    "uid": "demo-api-latency",
                    "title": "Demo API Latency",
                    "url": None,
                },
            ],
        )

    def test_get_dashboard_returns_dashboard_detail(self) -> None:
        client = self.create_client()

        response = client.get("/api/grafana/dashboards/demo-system-overview")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "uid": "demo-system-overview",
                "title": "Demo System Overview",
                "panels": ["API latency", "Worker health", "Error rate"],
            },
        )

    def test_get_dashboard_returns_404_when_missing(self) -> None:
        client = self.create_client()

        response = client.get("/api/grafana/dashboards/missing")

        self.assertEqual(response.status_code, 404)
        self.assertIn("missing", response.json()["detail"])

    def test_metrics_summary_returns_safe_operational_snapshot(self) -> None:
        client = self.create_client()

        response = client.get("/api/metrics/summary")

        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["source"], "fake_metrics")
        self.assertGreaterEqual(len(body["signals"]), 4)
        self.assertEqual(body["signals"][0]["name"], "database")
        self.assertEqual(body["signals"][0]["status"], "healthy")

    def test_metrics_signals_returns_safe_operational_signals(self) -> None:
        client = self.create_client()

        response = client.get("/api/metrics/signals")

        self.assertEqual(response.status_code, 200)
        signals = response.json()
        worker_queue = next(signal for signal in signals if signal["name"] == "worker_queue")
        self.assertEqual(worker_queue["status"], "degraded")
        self.assertEqual(worker_queue["severity"], "warning")
        self.assertEqual(worker_queue["trend"], "increasing")
        self.assertIn("synthetic", worker_queue["summary"])

    def test_operations_explanations_returns_safe_explanations(self) -> None:
        client = self.create_client()

        response = client.get("/api/operations/explanations")

        self.assertEqual(response.status_code, 200)
        explanations = response.json()
        worker_queue = next(
            explanation
            for explanation in explanations
            if explanation["signal"] == "worker_queue"
        )
        self.assertIn("Jobs are waiting", worker_queue["meaning"])
        self.assertIn("check worker health", worker_queue["recommended_checks"])
        self.assertIn(
            "restart production automatically",
            worker_queue["unsafe_actions"],
        )
        self.assertEqual(worker_queue["confidence"], "high")

    def test_operation_explanation_returns_one_signal_explanation(self) -> None:
        client = self.create_client()

        response = client.get("/api/operations/explanations/worker_queue")

        self.assertEqual(response.status_code, 200)
        explanation = response.json()
        self.assertEqual(explanation["signal"], "worker_queue")
        self.assertIn("background work", explanation["risk"])

    def test_operation_explanation_returns_404_when_signal_is_missing(self) -> None:
        client = self.create_client()

        response = client.get("/api/operations/explanations/missing_signal")

        self.assertEqual(response.status_code, 404)
        self.assertIn("missing_signal", response.json()["detail"])

    def test_maintenance_plan_returns_advisory_plan(self) -> None:
        client = self.create_client()

        response = client.get("/api/maintenance/plan")

        self.assertEqual(response.status_code, 200)
        plan = response.json()
        self.assertEqual(plan["title"], "Worker Queue Maintenance Plan")
        self.assertEqual(plan["priority"], "medium")
        self.assertTrue(
            any(step["requires_approval"] for step in plan["steps"]),
        )

    def test_signal_maintenance_plan_returns_one_signal_plan(self) -> None:
        client = self.create_client()

        response = client.get("/api/maintenance/plan/worker_queue")

        self.assertEqual(response.status_code, 200)
        plan = response.json()
        self.assertEqual(plan["title"], "Worker Queue Maintenance Plan")
        self.assertEqual(plan["steps"][0]["kind"], "check")

    def test_signal_maintenance_plan_returns_404_when_signal_is_missing(self) -> None:
        client = self.create_client()

        response = client.get("/api/maintenance/plan/missing_signal")

        self.assertEqual(response.status_code, 404)
        self.assertIn("missing_signal", response.json()["detail"])

    def test_action_proposals_returns_reviewable_proposals(self) -> None:
        client = self.create_client()

        response = client.get("/api/actions/proposals")

        self.assertEqual(response.status_code, 200)
        proposals = response.json()
        capacity_review = proposals[0]
        self.assertEqual(capacity_review["title"], "Review worker capacity")
        self.assertEqual(capacity_review["proposal_type"], "capacity_review")
        self.assertEqual(capacity_review["risk"], "medium")
        self.assertTrue(capacity_review["approval_required"])
        self.assertIn("worker_queue status is degraded", capacity_review["evidence"])
        self.assertIn(
            "do not restart workers automatically",
            capacity_review["must_not_execute"],
        )

    def test_signal_action_proposals_returns_signal_specific_proposals(self) -> None:
        client = self.create_client()

        response = client.get("/api/actions/proposals/api_latency")

        self.assertEqual(response.status_code, 200)
        proposals = response.json()
        self.assertEqual(len(proposals), 1)
        self.assertEqual(proposals[0]["proposal_type"], "threshold_review")
        self.assertFalse(proposals[0]["approval_required"])

    def test_signal_action_proposals_returns_404_when_signal_is_missing(self) -> None:
        client = self.create_client()

        response = client.get("/api/actions/proposals/missing_signal")

        self.assertEqual(response.status_code, 404)
        self.assertIn("missing_signal", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
