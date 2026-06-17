# How To Demo Hermes

This guide explains how to present Hermes to another person.

It is written for interviews, portfolio reviews, and open-source visitors.

## One Sentence

```text
Hermes is a Docker-first bounded observability agent that reads safe signals,
explains them, generates maintenance plans, and proposes human-reviewable
actions without executing infrastructure changes.
```

## What To Say First

Start with the boundary.

```text
Hermes is not an unrestricted automation agent.
It is intentionally bounded.
The public demo uses synthetic data.
Private deployments would inject real configuration outside Git.
```

This immediately shows security awareness.

## Demo Setup

Run the demo through Docker:

```bash
docker compose -f docker-compose.demo.yml up --build
```

Then open:

```text
http://localhost:8790/docs
```

The OpenAPI page lets a visitor inspect the endpoints without needing extra tooling.

## Demo Flow

Use this sequence:

```text
GET /health
GET /api/grafana/search
GET /api/metrics/signals
GET /api/operations/explanations/worker_queue
GET /api/maintenance/plan/worker_queue
GET /api/actions/proposals/worker_queue
```

This sequence is deliberate.

It shows Hermes becoming more helpful step by step.

## Step 1: Health

Endpoint:

```text
GET /health
```

What it proves:

- Hermes is running
- Docker runtime guard is active
- the selected Grafana source is visible

What to say:

```text
This confirms the service is up and tells us which source adapter is active.
For the public demo, the source is fake and safe.
```

## Step 2: Grafana Context

Endpoint:

```text
GET /api/grafana/search
```

What it proves:

- Hermes can expose safe dashboard metadata
- the public demo does not require a private Grafana instance
- the capability is read-only

What to say:

```text
This models the first capability, grafana.read.
It reads selected dashboard context but cannot mutate dashboards.
```

## Step 3: Operational Signals

Endpoint:

```text
GET /api/metrics/signals
```

What it proves:

- Hermes reads interpreted operational signals
- the public data is synthetic
- raw Prometheus data is not exposed

What to say:

```text
Hermes does not expose raw monitoring data.
It reads bounded operational signals such as database health, API latency,
worker queue pressure, and scrape target health.
```

## Step 4: Explanation

Endpoint:

```text
GET /api/operations/explanations/worker_queue
```

What it proves:

- Hermes explains what a signal means
- possible causes are hypotheses
- safe and unsafe actions are separated

What to say:

```text
Hermes explains the signal but does not claim a proven root cause.
It recommends checks and explicitly lists what it must not do automatically.
```

## Step 5: Maintenance Plan

Endpoint:

```text
GET /api/maintenance/plan/worker_queue
```

What it proves:

- Hermes can organize follow-up work
- steps are ordered
- risk and approval are visible
- the output is advisory

What to say:

```text
This turns the explanation into a maintenance plan.
It includes checks, investigation, documentation, and a proposal step that
requires approval before any infrastructure change.
```

## Step 6: Action Proposals

Endpoint:

```text
GET /api/actions/proposals/worker_queue
```

What it proves:

- Hermes proposes concrete human-reviewed actions
- evidence and preconditions are visible
- risky proposals require approval
- forbidden automatic actions are explicit

What to say:

```text
This is still not execution.
Hermes proposes a capacity review with evidence, preconditions, approval
requirements, and explicit actions it must not execute.
```

## What To Emphasize

Emphasize these ideas:

- Docker-first execution
- hexagonal architecture
- explicit ports and adapters
- fake public adapters
- private application boundary
- no secrets in Git
- no mutation endpoints
- no automatic remediation
- tests through Docker

## What Not To Overclaim

Do not say:

```text
Hermes fixes production issues automatically.
Hermes controls infrastructure.
Hermes connects directly to every private system.
Hermes knows the root cause from one signal.
```

Say:

```text
Hermes helps read, explain, plan, and propose.
Human approval remains required before operational changes.
```

## Close The Demo

Stop the demo:

```bash
docker compose -f docker-compose.demo.yml down
```

Then say:

```text
The current version deliberately stops at proposals.
The next step is not more power, but public hardening, graph refresh, and
careful review before connecting private deployments.
```
