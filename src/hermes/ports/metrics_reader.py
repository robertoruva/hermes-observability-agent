from typing import Protocol

from hermes.domain.metrics import MetricsSnapshot, OperationalSignal


class MetricsReader(Protocol):
    """Read-only port for safe operational metric summaries."""

    def read_snapshot(self) -> MetricsSnapshot:
        """Return a bounded snapshot of safe operational signals."""

    def list_signals(self) -> list[OperationalSignal]:
        """Return safe operational signals visible to Hermes."""
