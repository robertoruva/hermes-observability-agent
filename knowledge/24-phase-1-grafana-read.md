# Phase 1: Grafana Read

Phase 1 establishes the first bounded Hermes capability:

```text
grafana.read
```

This phase proves the core idea of Hermes:

```text
read operational context
-> keep the scope explicit
-> avoid write permissions
-> remain public-safe by default
```

## Purpose

The purpose of this phase is not to control Grafana.

The purpose is to let Hermes read a small, safe view of Grafana-style information.

Hermes can:

- check whether the configured Grafana source is reachable
- list available dashboards
- read one dashboard summary/detail

Hermes cannot:

- create dashboards
- edit dashboards
- delete dashboards
- manage users
- manage teams
- manage datasources
- run unrestricted queries
- expose private production configuration

## Why This Phase Comes First

Grafana is a good first capability because it is familiar in infrastructure teams and naturally read-oriented.

It also gives Hermes a practical foundation:

- health checks
- dashboard discovery
- operational visibility
- safe public demo data
- private integration path later

Starting with a small read-only capability keeps the agent understandable and safe.

## Public Implementation

The public repository implements the capability with fake adapters first.

This is intentional.

Fake adapters allow the project to:

- run without private infrastructure
- provide deterministic tests
- avoid real tokens
- avoid real dashboard data
- demonstrate the architecture publicly

Current public-safe sources:

```text
fake_grafana
fake_application_api
```

## Private Integration Path

The private integration path is:

```text
Hermes -> existing application API -> filtered Grafana/observability data
```

This avoids giving Hermes direct unrestricted access to private infrastructure.

The existing application remains responsible for:

- authentication
- authorization
- audit logging
- filtering sensitive information
- deciding which dashboards are safe to expose

The contract is documented in:

```text
knowledge/20-application-api-contract.md
```

## HTTP Surface

Phase 1 exposes a small HTTP surface:

```text
GET /health
GET /api/grafana/search
GET /api/grafana/dashboards/{uid}
```

These endpoints are read-only.

They return bounded DTOs, not raw private infrastructure responses.

## Configuration

The active Grafana source is selected with:

```text
HERMES_GRAFANA_SOURCE
```

Allowed values:

```text
fake_grafana
fake_application_api
application_api
```

The real application API source requires:

```text
HERMES_APPLICATION_API_BASE_URL
```

Real values belong in private files only:

```text
.env
docker-compose.override.yml
```

## Validation In This Phase

Current tests verify:

- use cases call the `GrafanaReader` port
- fake adapters return safe demo data
- adapter selection is explicit
- invalid configuration is rejected
- the real-shape application API adapter uses the expected internal contract
- missing dashboards become a domain-level `DashboardNotFound`
- the HTTP API returns safe read-only responses for health, search, dashboard detail, and missing dashboards

HTTP tests use FastAPI/Starlette's `TestClient`, backed by the development-only `httpx2` dependency.

## Phase 1 Completion Criteria

Phase 1 is considered complete when:

- `grafana.read` is the only implemented capability
- all endpoints are read-only
- fake demo mode works without private configuration
- Docker demo runs without real secrets
- the HTTP service is Docker-first and refuses to start without the Docker runtime marker
- the application API contract is documented
- adapter selection is explicit and tested
- public documentation explains why the scope is limited

## Next Phase

The recommended next capability is:

```text
metrics.read
```

That phase should follow the same pattern:

```text
domain model
-> port
-> use case
-> fake adapter
-> application API adapter
-> HTTP endpoint
-> tests
-> knowledge note
```

Hermes should continue to recommend and explain before it ever executes operational actions.
