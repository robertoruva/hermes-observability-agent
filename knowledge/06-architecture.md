# Architecture

Hermes Observability Agent is planned as a hexagonal application.

The core should not depend on Grafana, Docker, FastAPI, or any specific deployment mechanism.

## Planned Structure

```text
src/
  domain/
  application/
  ports/
  infrastructure/
  interfaces/
```

## Dependency Direction

```text
interfaces -> application -> ports/domain
infrastructure -> ports/domain
```

The application layer depends on abstractions. Infrastructure implements those abstractions.

## First Adapter

The first infrastructure adapter will be a Grafana HTTP client implementing a read-only port.

```text
GrafanaReader
```

The HTTP API will call application use cases, not the Grafana client directly.

## Why This Architecture

Hexagonal architecture helps Hermes stay testable, explainable, and extensible.

For example, tests can replace the real Grafana adapter with a fake in-memory adapter. Future capabilities can be added without rewriting the core.
