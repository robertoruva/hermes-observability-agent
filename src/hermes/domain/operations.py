from dataclasses import dataclass
from enum import StrEnum


class ExplanationConfidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class OperationalExplanation:
    signal: str
    meaning: str
    risk: str
    possible_causes: tuple[str, ...]
    recommended_checks: tuple[str, ...]
    safe_actions: tuple[str, ...]
    unsafe_actions: tuple[str, ...]
    confidence: ExplanationConfidence
