import unittest

from hermes.application.use_cases.list_operational_signals import ListOperationalSignals
from hermes.application.use_cases.read_metrics_snapshot import ReadMetricsSnapshot
from hermes.domain.metrics import SignalSeverity, SignalStatus, TrendDirection
from hermes.infrastructure.metrics.fake_metrics_reader import FakeMetricsReader


class MetricsUseCasesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.reader = FakeMetricsReader()

    def test_read_metrics_snapshot(self) -> None:
        snapshot = ReadMetricsSnapshot(self.reader).execute()

        self.assertEqual(snapshot.source, "fake_metrics")
        self.assertGreaterEqual(len(snapshot.signals), 4)
        self.assertEqual(snapshot.signals[0].name, "database")
        self.assertEqual(snapshot.signals[0].status, SignalStatus.HEALTHY)

    def test_list_operational_signals(self) -> None:
        signals = ListOperationalSignals(self.reader).execute()

        worker_queue = next(signal for signal in signals if signal.name == "worker_queue")

        self.assertEqual(worker_queue.status, SignalStatus.DEGRADED)
        self.assertEqual(worker_queue.severity, SignalSeverity.WARNING)
        self.assertEqual(worker_queue.trend, TrendDirection.INCREASING)
        self.assertIn("synthetic", worker_queue.summary)


if __name__ == "__main__":
    unittest.main()
