# Hermes Observability Agent

Hermes is a Docker-first bounded observability agent.

It reads safe operational context, explains what it sees, generates maintenance plans, and proposes human-reviewable actions.

It does **not** execute infrastructure changes.

```text
read
-> explain
-> plan
-> propose
-> wait for approval
```

That is the core idea: useful operational intelligence without uncontrolled automation.

## Why Hermes Exists

Modern teams often have dashboards, metrics, queues, alerts, and admin panels, but reading them well is still hard.

Hermes explores a safer agent pattern:

- read bounded observability data
- explain operational signals in plain language
- separate hypotheses from facts
- generate maintenance plans
- propose next actions for human review
- keep execution outside the agent

The public repository is intentionally educational and safe to run.

It uses fake adapters and synthetic data. No real Grafana instance, Prometheus instance, private application, LLM key, or production token is required.

## What You Can Demo

The public demo tells a complete story:

```text
GET /health
GET /api/grafana/search
GET /api/metrics/signals
GET /api/operations/explanations/worker_queue
GET /api/maintenance/plan/worker_queue
GET /api/actions/proposals/worker_queue
```

That flow shows Hermes moving from basic availability to a concrete, reviewable proposal.

Example proposal:

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

Notice the shape: evidence, risk, approval, and explicit forbidden actions.

Hermes proposes. A human decides.

## Quick Start

Run the test suite:

```bash
docker compose -f docker-compose.test.yml run --rm hermes-test
```

Run the demo:

```bash
docker compose -f docker-compose.demo.yml up --build
```

Then open:

```text
http://localhost:8790/docs
```

Useful demo URLs:

```text
http://localhost:8790/health
http://localhost:8790/api/grafana/search
http://localhost:8790/api/metrics/signals
http://localhost:8790/api/actions/proposals/worker_queue
```

Stop the demo:

```bash
docker compose -f docker-compose.demo.yml down
```

Hermes is Docker-first by design. The HTTP application refuses to start unless it is running inside the Hermes Docker runtime.

## Implemented Capabilities

Hermes currently implements this capability path:

```text
grafana.read
-> metrics.read
-> operations.explain
-> maintenance.plan.generate
-> actions.propose
```

| Capability | Status | What It Does |
| --- | --- | --- |
| `grafana.read` | Implemented | Reads safe Grafana-style dashboard context. |
| `metrics.read` | Implemented | Reads synthetic operational signals. |
| `operations.explain` | Implemented | Explains signal meaning, risk, possible causes, checks, and unsafe actions. |
| `maintenance.plan.generate` | Implemented | Turns explanations into advisory maintenance plans. |
| `actions.propose` | Implemented | Produces human-reviewable action proposals with evidence and preconditions. |

Execution remains out of scope.

## Architecture

Hermes follows hexagonal architecture:

```text
src/hermes/
  domain/
  application/
  ports/
  infrastructure/
  interfaces/
```

The important rule is simple:

```text
domain and use cases do not depend on FastAPI, Docker, Grafana, or private infrastructure
```

Ports describe what Hermes needs.

Adapters decide where the data comes from.

That makes the public demo fake and deterministic while leaving a clean path for private integrations later.

## Public By Design, Private By Configuration

The public repository contains:

- reusable architecture
- synthetic data
- fake adapters
- Docker workflows
- tests
- knowledge notes
- generated graph artifacts

Private deployments provide:

- real URLs
- real tokens
- real dashboards
- real application API endpoints
- optional private LLM behavior
- environment-specific configuration

Private configuration belongs outside Git:

```text
.env
docker-compose.override.yml
```

Those files are ignored on purpose.

## What Hermes Will Not Do

Hermes does not:

- execute commands
- restart services
- scale workers
- edit infrastructure
- silence alerts
- delete data
- mutate Grafana dashboards
- expose raw Prometheus data
- expose private logs
- require a public LLM API key

This is not a missing feature list.

It is the safety model.

## Demo Source Selection

The public demo uses fake data by default:

```text
HERMES_GRAFANA_SOURCE=fake_grafana
```

Supported values:

```text
fake_grafana
fake_application_api
application_api
```

The real `application_api` source requires `HERMES_APPLICATION_API_BASE_URL` and is intended for private configuration only.

## Knowledge Tree

Hermes includes a learning-oriented knowledge tree:

```text
knowledge/
```

Start here:

```text
knowledge/23-why-these-files-exist.md
knowledge/30-roadmap-and-learning-path.md
knowledge/22-capability-matrix.md
```

Read the implemented phases:

```text
knowledge/24-phase-1-grafana-read.md
knowledge/26-phase-2-metrics-read.md
knowledge/27-phase-3-operations-explain.md
knowledge/28-phase-4-maintenance-plan-generate.md
knowledge/29-phase-5-actions-propose.md
```

Read the practical guides:

```text
knowledge/31-how-to-read-operational-signals.md
knowledge/32-how-to-read-operational-explanations.md
knowledge/33-how-to-read-action-proposals.md
knowledge/35-how-to-demo-hermes.md
```

Read the release and safety decisions:

```text
knowledge/34-public-demo-hardening.md
knowledge/36-public-release-checklist.md
knowledge/37-llm-private-layer-decision.md
```

## Knowledge Graph

The generated knowledge graph is included so visitors can explore the architecture visually:

```text
graphify-out/graph.html
```

The report is here:

```text
graphify-out/GRAPH_REPORT.md
```

The current graph includes the capability pipeline, Docker runtime, public safety model, release readiness, implementation surface, and demo story.

## Governance

Project governance:

```text
LICENSE
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
```

Please do not publish real secrets, private URLs, production screenshots, customer data, raw logs, or infrastructure details in issues or pull requests.

## Interview Pitch

```text
Hermes is a Docker-first bounded observability agent.
It reads safe operational signals, explains them, turns them into maintenance
plans, and proposes human-reviewable actions.
It uses hexagonal architecture so the public demo can stay fake and safe while
private deployments can inject real application API context later.
Execution is intentionally out of scope.
```

That is the point of the project: operational usefulness with visible boundaries.
