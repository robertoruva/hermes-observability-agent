from typing import Protocol

from hermes.domain.actions import ActionProposal
from hermes.domain.maintenance import MaintenancePlan


class ActionProposer(Protocol):
    """Propose human-reviewable actions without executing them."""

    def propose_actions(self, plan: MaintenancePlan) -> list[ActionProposal]:
        """Return bounded proposals for a maintenance plan."""
