from urllib.parse import quote


GRAFANA_HEALTH_PATH = "/internal/hermes/grafana/health"
GRAFANA_SEARCH_PATH = "/internal/hermes/grafana/search"


def grafana_dashboard_path(uid: str) -> str:
    return f"/internal/hermes/grafana/dashboards/{quote(uid, safe='')}"
