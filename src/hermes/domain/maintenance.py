from dataclasses import dataclass
from enum import StrEnum


class MaintenancePriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class StepKind(StrEnum):
    CHECK = "check"
    INVESTIGATION = "investigation"
    DOCUMENTATION = "documentation"
    PROPOSAL = "proposal"
    FOLLOW_UP = "follow_up"


class StepRisk(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class MaintenanceStep:
    order: int
    title: str
    kind: StepKind
    risk: StepRisk
    requires_approval: bool
    summary: str


@dataclass(frozen=True)
class MaintenancePlan:
    title: str
    priority: MaintenancePriority
    summary: str
    steps: tuple[MaintenanceStep, ...]
