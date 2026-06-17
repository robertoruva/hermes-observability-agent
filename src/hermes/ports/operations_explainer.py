from typing import Protocol

from hermes.domain.metrics import OperationalSignal
from hermes.domain.operations import OperationalExplanation


class OperationsExplainer(Protocol):
    """Explain safe operational signals without executing actions."""

    def explain(self, signal: OperationalSignal) -> OperationalExplanation:
        """Return a bounded explanation for one operational signal."""
