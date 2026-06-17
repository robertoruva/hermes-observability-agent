from typing import Protocol

from hermes.domain.maintenance import MaintenancePlan
from hermes.domain.operations import OperationalExplanation


class MaintenancePlanner(Protocol):
    """Generate advisory plans from explanations without executing actions."""

    def generate_plan(
        self,
        explanations: list[OperationalExplanation],
    ) -> MaintenancePlan:
        """Return a bounded maintenance plan."""
