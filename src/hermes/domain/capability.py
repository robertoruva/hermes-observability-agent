from dataclasses import dataclass


@dataclass(frozen=True)
class Capability:
    """A bounded action Hermes is allowed to perform."""

    name: str
    description: str
    read_only: bool = True
