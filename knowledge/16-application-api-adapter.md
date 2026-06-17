# Application API Adapter

Hermes can read observability data through the existing application instead of connecting directly to infrastructure.

This is represented by an application API adapter.

## Purpose

The adapter demonstrates this private shape:

```text
Hermes use case
-> Hermes port
-> application API adapter
-> existing application
-> Grafana/admin data
```

The existing application remains responsible for:

- permissions
- validation
- audit trail
- business rules
- infrastructure access

## Why This Matters

This keeps Hermes bounded.

Hermes does not need direct access to databases, servers, containers, or cloud infrastructure.

Instead, Hermes asks the application for selected information through a controlled API.

## Same Port, Different Adapter

The use cases depend on:

```text
GrafanaReader
```

The implementation can be:

```text
FakeGrafanaReader
FakeApplicationGrafanaReader
FutureRealApplicationGrafanaReader
FutureRealGrafanaReader
```

The use cases do not change.

This is the value of hexagonal architecture.

## Public Demo

The public repository uses a fake application API adapter.

It proves the architecture without exposing:

- private application URLs
- real tokens
- real dashboard data
- internal infrastructure details

## Private Future

In private use, the fake adapter can be replaced by a real adapter that calls the existing application.

Example:

```text
GET /internal/hermes/grafana/search
GET /internal/hermes/grafana/dashboards/{uid}
```

Those endpoints would belong to the existing application, not to Grafana directly.
