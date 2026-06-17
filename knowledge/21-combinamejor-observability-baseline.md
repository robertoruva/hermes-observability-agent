# CombinaMejor Observability Baseline

This note captures the private observability shape that Hermes should be compatible with later.

It is intentionally sanitized for the public Hermes repository. Do not copy real domains, tokens, passwords, customer data, screenshots, or production-only operational details here.

## Why This Matters

Hermes is being designed as a reusable open-source agent, but the first real private integration target is the existing application stack.

The goal is not for Hermes to own infrastructure.

The goal is for Hermes to read a controlled operational view through a narrow application boundary.

## Observed Private Shape

The private application already has an observability stack with these roles:

```text
application -> /internal/metrics -> prometheus -> grafana
```

The important pieces are:

- A Symfony application exposing Prometheus metrics through an internal endpoint.
- Prometheus scraping that endpoint with a bearer token.
- Grafana reading from Prometheus as its datasource.
- Grafana dashboards provisioned from files.
- Production ports for Prometheus and Grafana bound to localhost, not broadly exposed.
- Nginx proxying Grafana behind HTTPS under a subpath.

This is a good base for Hermes because the real data already flows through an observability layer.

## Current Metrics Boundary

The existing application exposes:

```text
GET /internal/metrics
```

This endpoint is protected in two ways:

- Network boundary: intended for internal Docker-network access.
- Token boundary: requires a bearer token.

The current metric families include application identity, database health, and PHP memory usage.

The exact metric names are private implementation details. Hermes should not hardcode private business assumptions in its open-source core.

## Current Grafana Shape

The private Grafana setup has:

- A Prometheus datasource.
- A provisioned overview dashboard.
- Panels for database health, PHP memory, RabbitMQ queue state, PostgreSQL exporter health, and scrape target health.

For Hermes, the useful public abstraction is:

```text
Dashboard summary:
- uid
- title
- url

Dashboard detail:
- uid
- title
- panels
```

That matches the current `grafana.read` port and keeps the public contract generic.

## Recommended Hermes Integration

Hermes should not connect directly to private databases, RabbitMQ, Redis, or production containers.

The recommended private path is:

```text
Hermes -> private application API -> Grafana/observability layer
```

This lets the existing application remain responsible for:

- Authentication.
- Authorization.
- Audit logging.
- Rate limiting.
- Filtering what operational data can be exposed.
- Hiding sensitive infrastructure details.

## Application API Contract Candidate

The currently documented Hermes contract remains a good candidate:

```text
GET /internal/hermes/grafana/health
GET /internal/hermes/grafana/search
GET /internal/hermes/grafana/dashboards/{uid}
```

In the private application, these endpoints can translate from the real Grafana setup into the safe Hermes DTOs.

Hermes should receive only the information it needs for `grafana.read`.

## Security Notes

Safe to expose in the public Hermes repository:

- Generic architecture.
- Synthetic examples.
- Contract shape.
- Read-only capability names.
- Fake dashboard data.

Not safe to expose:

- Real domains.
- Real Grafana admin credentials.
- Real bearer tokens.
- Private dashboard screenshots.
- Raw production metric output.
- Internal container names if they reveal private deployment details.
- Customer or user data.

## What This Confirms

The private stack supports the Hermes direction:

- FastAPI remains appropriate for Hermes because Hermes is an external bounded agent.
- The application API adapter remains appropriate because the existing application should own private access rules.
- The `grafana.read` port remains appropriately small.
- Docker is appropriate because Hermes can join the local/private environment later without becoming part of the main application.

## Next Step

Create a capability matrix for Hermes:

- What Hermes can do now.
- What Hermes cannot do by design.
- What future capabilities may be added.
- Which adapter would own each capability.

This will make the project easier to explain as an open-source architecture and safer to extend privately.
