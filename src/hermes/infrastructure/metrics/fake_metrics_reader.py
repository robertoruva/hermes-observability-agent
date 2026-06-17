from hermes.domain.metrics import (
    MetricsSnapshot,
    OperationalSignal,
    SignalSeverity,
    SignalStatus,
    TrendDirection,
)


class FakeMetricsReader:
    """Demo adapter for safe synthetic operational signals."""

    def __init__(self) -> None:
        self._signals = (
            OperationalSignal(
                name="database",
                status=SignalStatus.HEALTHY,
                severity=SignalSeverity.INFO,
                summary="Database is reachable.",
                trend=TrendDirection.STABLE,
            ),
            OperationalSignal(
                name="api_latency",
                status=SignalStatus.HEALTHY,
                severity=SignalSeverity.INFO,
                summary="API latency is stable in the public demo.",
                trend=TrendDirection.STABLE,
            ),
            OperationalSignal(
                name="worker_queue",
                status=SignalStatus.DEGRADED,
                severity=SignalSeverity.WARNING,
                summary="Queue depth is increasing slowly in the synthetic scenario.",
                trend=TrendDirection.INCREASING,
            ),
            OperationalSignal(
                name="scrape_targets",
                status=SignalStatus.HEALTHY,
                severity=SignalSeverity.INFO,
                summary="All synthetic scrape targets are reachable.",
                trend=TrendDirection.STABLE,
            ),
        )

    def read_snapshot(self) -> MetricsSnapshot:
        return MetricsSnapshot(source="fake_metrics", signals=self._signals)

    def list_signals(self) -> list[OperationalSignal]:
        return list(self._signals)
