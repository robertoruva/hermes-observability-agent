import os
from dataclasses import dataclass
from enum import StrEnum


class GrafanaSource(StrEnum):
    FAKE_GRAFANA = "fake_grafana"
    FAKE_APPLICATION_API = "fake_application_api"
    APPLICATION_API = "application_api"


@dataclass(frozen=True)
class HermesConfig:
    grafana_source: GrafanaSource = GrafanaSource.FAKE_GRAFANA
    application_api_base_url: str | None = None
    application_api_timeout_seconds: float = 2.0


def load_config() -> HermesConfig:
    config = HermesConfig(
        grafana_source=parse_grafana_source(
            os.getenv("HERMES_GRAFANA_SOURCE", GrafanaSource.FAKE_GRAFANA.value)
        ),
        application_api_base_url=normalize_optional_url(
            os.getenv("HERMES_APPLICATION_API_BASE_URL")
        ),
        application_api_timeout_seconds=parse_positive_float(
            os.getenv("HERMES_APPLICATION_API_TIMEOUT_SECONDS", "2.0"),
            "HERMES_APPLICATION_API_TIMEOUT_SECONDS",
        ),
    )
    validate_config(config)
    return config


def parse_grafana_source(value: str) -> GrafanaSource:
    try:
        return GrafanaSource(value)
    except ValueError as exc:
        allowed = ", ".join(source.value for source in GrafanaSource)
        raise InvalidHermesConfig(
            f"Invalid HERMES_GRAFANA_SOURCE={value!r}. Allowed values: {allowed}."
        ) from exc


class InvalidHermesConfig(ValueError):
    """Raised when Hermes receives unsupported configuration."""


def normalize_optional_url(value: str | None) -> str | None:
    if value is None or value.strip() == "":
        return None
    return value.strip().rstrip("/")


def parse_positive_float(value: str, name: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise InvalidHermesConfig(f"Invalid {name}={value!r}. Expected a number.") from exc

    if parsed <= 0:
        raise InvalidHermesConfig(f"Invalid {name}={value!r}. Expected a positive number.")

    return parsed


def validate_config(config: HermesConfig) -> None:
    if (
        config.grafana_source == GrafanaSource.APPLICATION_API
        and config.application_api_base_url is None
    ):
        raise InvalidHermesConfig(
            "HERMES_APPLICATION_API_BASE_URL is required when "
            "HERMES_GRAFANA_SOURCE='application_api'."
        )
