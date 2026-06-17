from dataclasses import dataclass
from enum import StrEnum


class SignalStatus(StrEnum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"


class SignalSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class TrendDirection(StrEnum):
    STABLE = "stable"
    INCREASING = "increasing"
    DECREASING = "decreasing"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class OperationalSignal:
    name: str
    status: SignalStatus
    severity: SignalSeverity
    summary: str
    trend: TrendDirection


@dataclass(frozen=True)
class MetricsSnapshot:
    source: str
    signals: tuple[OperationalSignal, ...]
