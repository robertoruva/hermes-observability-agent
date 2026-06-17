from dataclasses import dataclass
from enum import StrEnum


class ProposalRisk(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ProposalType(StrEnum):
    CAPACITY_REVIEW = "capacity_review"
    RUNBOOK_DOCUMENTATION = "runbook_documentation"
    THRESHOLD_REVIEW = "threshold_review"
    DASHBOARD_COVERAGE_REVIEW = "dashboard_coverage_review"
    GENERAL_REVIEW = "general_review"


@dataclass(frozen=True)
class ActionProposal:
    title: str
    proposal_type: ProposalType
    reason: str
    evidence: tuple[str, ...]
    preconditions: tuple[str, ...]
    approval_required: bool
    risk: ProposalRisk
    human_action: str
    must_not_execute: tuple[str, ...]
