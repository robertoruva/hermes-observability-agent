# Open Source Strategy

Hermes should be designed as an open source project that is useful for other people while still being safe for private use.

The goal is not to publish a private deployment. The goal is to publish a reusable core.

## Public Core, Private Configuration

Hermes can be public because the repository should contain only:

- generic source code
- architecture documentation
- tests
- synthetic demo data
- example configuration
- Docker demo files

Private use should happen through local configuration that is not committed:

```text
.env
docker-compose.override.yml
```

This means the same open source code can be used in a private environment by injecting:

- private Grafana URL
- read-only Grafana token
- local port choices
- environment-specific settings

The public repository should never contain those values.

## Who Hermes Is For

Hermes is for developers and small teams that want a safe way to expose selected observability capabilities without giving broad access to infrastructure tools.

The first audience is:

- developers learning observability
- teams using Grafana
- people who want a small read-only operational gateway
- engineers who care about explicit boundaries and clean architecture

## Problem Statement

Grafana is powerful, but direct access can reveal too much or encourage broad permissions.

Hermes provides a smaller surface:

```text
client -> Hermes -> read-only capability -> Grafana
```

Instead of exposing everything Grafana can do, Hermes exposes only the use cases it explicitly supports.

## What Hermes Is Not

Hermes is not:

- a Grafana replacement
- a full monitoring platform
- an admin console
- a secret store
- a generic unrestricted proxy

Hermes should avoid becoming a tool that can do anything.

Its value comes from being intentionally bounded.

## Open Source Quality Bar

For Hermes to feel like a real open source project, it should include:

- clear README
- license
- contribution guide
- security policy
- reproducible demo
- safe example configuration
- tests
- roadmap
- architecture notes

The project should be easy to inspect, easy to run, and hard to misuse accidentally.

## Roadmap

### v0.1

- read-only Grafana capability
- HTTP API
- Docker container
- synthetic Grafana demo
- basic tests
- public documentation

### v0.2

- stronger capability registry
- better error handling
- typed configuration
- more test coverage
- example dashboards

### v0.3

- additional read-only capabilities
- optional auth in front of Hermes
- deployment examples
- richer knowledge graph

## Interview Explanation

Hermes is open source by design, but private by configuration.

The repository demonstrates the architecture and contains a safe demo. Real deployments inject private URLs and tokens through ignored local files.

This allows Hermes to be useful publicly without exposing private infrastructure.
