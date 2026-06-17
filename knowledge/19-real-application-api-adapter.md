# Real Application API Adapter

Hermes now has the shape of a real adapter for the existing application boundary.

This adapter is called:

```text
ApplicationApiGrafanaReader
```

It implements the same port as the fake adapters:

```text
GrafanaReader
```

## Purpose

The adapter prepares Hermes for private use without giving it direct infrastructure access.

The intended private shape is:

```text
Hermes
-> ApplicationApiGrafanaReader
-> existing application internal API
-> Grafana/admin data
```

## Expected Application Endpoints

The adapter expects the existing application to expose selected read-only endpoints:

```text
GET /internal/hermes/grafana/health
GET /internal/hermes/grafana/search
GET /internal/hermes/grafana/dashboards/{uid}
```

These endpoints should belong to the existing application.

Hermes should not bypass them to reach private infrastructure directly.

The detailed contract is documented in:

```text
knowledge/20-application-api-contract.md
```

## Configuration

The real adapter is selected with:

```text
HERMES_GRAFANA_SOURCE=application_api
```

It also requires:

```text
HERMES_APPLICATION_API_BASE_URL
```

Example public placeholder:

```text
HERMES_APPLICATION_API_BASE_URL=http://localhost:8000
```

Real private URLs must live only in ignored local files.

## Current Safety

The public repository does not call a real private application.

Tests mock the HTTP layer.

The Docker demo still defaults to:

```text
HERMES_GRAFANA_SOURCE=fake_grafana
```

## Why This Matters

This step proves the production direction without exposing private systems.

Hermes can now support three shapes:

```text
fake_grafana
fake_application_api
application_api
```

Only the first two are public demo modes.

The real `application_api` mode is for private configuration.
