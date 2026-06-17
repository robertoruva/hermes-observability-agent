# Hermes Observability Agent

Hermes Observability Agent is a Docker-first bounded observability agent.

It reads safe operational context, explains signals, generates maintenance plans, and proposes human-reviewable actions.

It does not execute infrastructure changes.

This repository is intended to be public and educational. It must never contain real production tokens, private Grafana URLs, customer data, internal infrastructure names, or screenshots from private systems.

Hermes is Docker-first by design. The supported way to run and test the service is through the provided Docker Compose files, and the HTTP application refuses to start unless it is running inside the Hermes Docker runtime.

## Goals

- Build Hermes as a bounded agent with explicit capabilities.
- Keep the architecture hexagonal: domain and use cases stay independent from HTTP, Docker, and Grafana.
- Provide a reproducible public demo with synthetic data.
- Keep private deployments externalized through environment variables and ignored local files.
- Document the reasoning so the project can be explained clearly in interviews or engineering reviews.

## Open Source

Hermes is intended to be open source by design and private by configuration.

The public repository contains the reusable core, safe examples, and synthetic demo material. Private deployments inject real URLs, tokens, and environment-specific settings through ignored local files.

Project governance:

```text
LICENSE
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
```

## First Capability

```text
grafana.read
```

Hermes should be able to:

- Check whether Grafana is reachable.
- Search dashboards.
- Read dashboard definitions.

Hermes should not be able to:

- Create, update, or delete dashboards.
- Manage users or teams.
- Change datasources.
- Access private production configuration from the public repository.

## Public vs Private

The public repository contains generic code, documentation, tests, and synthetic demo data.

Private configuration lives outside Git:

```text
.env
docker-compose.override.yml
```

Those files are ignored on purpose.

For private deployments, Hermes should prefer controlled application APIs over direct infrastructure access. The existing application should remain the owner of business rules, permissions, validation, and audit trails.

## Current Implementation

Hermes now includes a first hexagonal skeleton:

```text
src/hermes/
  domain/
  application/
  ports/
  infrastructure/
  interfaces/
```

The current infrastructure adapter is fake on purpose. It lets the application demonstrate the read-only Grafana flow without using real URLs, tokens, or private dashboards.

The code also includes a fake application API adapter to model the preferred private shape: Hermes talks to a controlled application boundary, and the existing application remains responsible for permissions, validation, and infrastructure access.

Hermes also includes a public-safe `metrics.read` implementation with synthetic operational signals.

Hermes also includes a public-safe `operations.explain` implementation with deterministic explanations for those synthetic signals.

Hermes also includes a public-safe `maintenance.plan.generate` implementation that turns explanations into advisory maintenance plans.

Hermes also includes a public-safe `actions.propose` implementation that turns advisory plans into human-reviewable action proposals.

The expected private application contract is documented in `knowledge/20-application-api-contract.md`.

The implemented capability path is:

```text
grafana.read
-> metrics.read
-> operations.explain
-> maintenance.plan.generate
-> actions.propose
```

Choose the current demo source with:

```text
HERMES_GRAFANA_SOURCE=fake_grafana
HERMES_GRAFANA_SOURCE=fake_application_api
HERMES_GRAFANA_SOURCE=application_api
```

Hermes validates this value at startup and rejects unsupported sources. The real `application_api` source requires `HERMES_APPLICATION_API_BASE_URL` and is intended for private configuration only.

Run the test suite with Docker:

```bash
docker compose -f docker-compose.test.yml run --rm hermes-test
```

Run the Docker demo:

```bash
docker compose -f docker-compose.demo.yml up --build
```

Then open:

```text
http://localhost:8790/health
http://localhost:8790/api/grafana/search
http://localhost:8790/docs
```

Available demo endpoints:

```text
GET /health
GET /api/grafana/search
GET /api/grafana/dashboards/demo-system-overview
GET /api/metrics/summary
GET /api/metrics/signals
GET /api/operations/explanations
GET /api/operations/explanations/worker_queue
GET /api/maintenance/plan
GET /api/maintenance/plan/worker_queue
GET /api/actions/proposals
GET /api/actions/proposals/worker_queue
```

Suggested demo flow:

```text
1. GET /health
2. GET /api/grafana/search
3. GET /api/metrics/signals
4. GET /api/operations/explanations/worker_queue
5. GET /api/maintenance/plan/worker_queue
6. GET /api/actions/proposals/worker_queue
```

Example proposal response shape:

```json
{
  "title": "Review worker capacity",
  "proposal_type": "capacity_review",
  "approval_required": true,
  "risk": "medium",
  "evidence": [
    "worker_queue status is degraded",
    "worker_queue trend is increasing"
  ],
  "must_not_execute": [
    "do not restart workers automatically",
    "do not change scaling automatically"
  ]
}
```

## Learning Path

Start with the knowledge tree:

```text
knowledge/
```

To understand why the main files and folders exist, see:

```text
knowledge/23-why-these-files-exist.md
```

To follow the roadmap and learning path, see:

```text
knowledge/30-roadmap-and-learning-path.md
```

The generated knowledge graph can be opened at:

```text
graphify-out/graph.html
```

To understand how to read it, see:

```text
knowledge/08-how-to-read-the-graph.md
```

To understand Hermes capabilities and boundaries, see:

```text
knowledge/22-capability-matrix.md
```

To understand the current first phase, see:

```text
knowledge/24-phase-1-grafana-read.md
```

To understand the planned second phase, see:

```text
knowledge/26-phase-2-metrics-read.md
```

To learn how to read the current synthetic operational signals, see:

```text
knowledge/31-how-to-read-operational-signals.md
```

To understand the current third phase, see:

```text
knowledge/27-phase-3-operations-explain.md
```

To learn how to read operational explanations, see:

```text
knowledge/32-how-to-read-operational-explanations.md
```

To understand the current fourth phase, see:

```text
knowledge/28-phase-4-maintenance-plan-generate.md
```

To understand the current fifth phase, see:

```text
knowledge/29-phase-5-actions-propose.md
```

To learn how to read action proposals, see:

```text
knowledge/33-how-to-read-action-proposals.md
```

To understand the current consolidation phase, see:

```text
knowledge/34-public-demo-hardening.md
```

To learn how to present the project, see:

```text
knowledge/35-how-to-demo-hermes.md
```

To review the public release checklist, see:

```text
knowledge/36-public-release-checklist.md
```

To understand why LLM usage is private and optional, see:

```text
knowledge/37-llm-private-layer-decision.md
```

The current implementation intentionally uses fake and synthetic adapters so the architecture can be understood before connecting private infrastructure.
