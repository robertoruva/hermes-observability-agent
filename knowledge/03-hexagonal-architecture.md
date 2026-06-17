# Hexagonal Architecture

Hermes should use hexagonal architecture so the core business logic does not depend on external tools.

The main idea is simple:

The application defines what it needs. Infrastructure provides how it is done.

## Layers

```text
domain
application
ports
infrastructure
interfaces
```

## Domain

The domain contains the concepts Hermes cares about:

- capability
- dashboard
- panel
- health status

The domain should not know about HTTP, FastAPI, Docker, or Grafana's API format.

## Application

The application layer contains use cases:

- check Grafana health
- search dashboards
- get dashboard by UID

Use cases coordinate work, but they still avoid direct dependency on Grafana.

## Ports

Ports are interfaces that describe what the application needs.

Example:

```text
GrafanaReader
```

It can define operations such as:

```text
search_dashboards
get_dashboard
check_health
```

## Infrastructure

Infrastructure implements ports using real external tools.

For the first capability, this means an HTTP client that talks to Grafana.

## Interfaces

Interfaces expose Hermes to the outside world.

The first interface will be an HTTP API.

Later, Hermes could also expose a CLI, scheduled jobs, or agent workflows without changing the core use cases.
