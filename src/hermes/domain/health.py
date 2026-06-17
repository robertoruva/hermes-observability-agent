from dataclasses import dataclass


@dataclass(frozen=True)
class HealthStatus:
    service: str
    reachable: bool
    message: str
