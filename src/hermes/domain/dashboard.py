from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardSummary:
    uid: str
    title: str
    url: str | None = None


@dataclass(frozen=True)
class Dashboard:
    uid: str
    title: str
    panels: tuple[str, ...] = ()
