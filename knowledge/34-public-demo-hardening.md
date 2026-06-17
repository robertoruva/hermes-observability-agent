# Public Demo Hardening

This consolidation phase prepares Hermes to be shown publicly.

The goal is not to add more operational power.

The goal is to make the current project safer, clearer, easier to run, and easier to explain.

## Why This Phase Exists

Hermes already implements the first useful learning path:

```text
grafana.read
-> metrics.read
-> operations.explain
-> maintenance.plan.generate
-> actions.propose
```

That is enough capability to demonstrate the architecture.

Adding more features too early would make the project harder to understand.

Consolidation makes the current work trustworthy.

## Consolidation Goals

This phase should improve:

- first-time reader experience
- public demo clarity
- security confidence
- endpoint examples
- interview readiness
- knowledge graph freshness
- private/public separation

## What Should Be Checked

Before publishing or sharing the repository, check:

- the README explains the value quickly
- Docker commands are the only supported run path
- demo endpoints use synthetic data
- no real tokens are present
- no private URLs are present
- no private screenshots are present
- no customer data is present
- `.env` and private overrides stay ignored
- tests pass in Docker
- the knowledge graph reflects the current project
- the public repository does not require an LLM API key

## Public Demo Story

The public demo should tell this story:

```text
Hermes is a Docker-first bounded observability agent.
It reads safe operational data, explains it, generates maintenance plans,
and proposes human-reviewable actions.
It never executes infrastructure changes.
```

That story is important because it shows:

- observability understanding
- safety boundaries
- hexagonal architecture
- Docker reproducibility
- public/private separation
- professional communication

## Recommended Demo Flow

The demo should be shown in this order:

```text
GET /health
GET /api/grafana/search
GET /api/metrics/signals
GET /api/operations/explanations/worker_queue
GET /api/maintenance/plan/worker_queue
GET /api/actions/proposals/worker_queue
```

This order mirrors Hermes's learning path:

```text
available
-> dashboard context
-> operational signal
-> explanation
-> plan
-> proposal
```

## What Must Stay Out Of Scope

Consolidation must not add:

- execution endpoints
- mutation endpoints
- real infrastructure credentials
- raw Prometheus access
- raw log access
- private application names
- private deployment details
- public LLM provider requirements

Hermes should remain safe to download and run publicly.

## Public Checklist

Before sharing Hermes, run:

```bash
docker compose -f docker-compose.test.yml run --rm hermes-test
docker compose -f docker-compose.demo.yml up --build
```

Then check:

- `/docs` opens
- `/api/actions/proposals/worker_queue` returns proposals
- proposals include `approval_required`
- proposals include `must_not_execute`
- demo data is synthetic
- the project can be explained without private context
- no LLM API key is needed for the public demo

After testing the demo, stop it:

```bash
docker compose -f docker-compose.demo.yml down
```

## Knowledge Graph Refresh

After consolidation docs are stable, regenerate the graph.

The graph should include:

- implemented phases
- public hardening
- action proposal reading guide
- demo guide
- Docker-first workflow
- security boundaries
- private optional LLM decision

This keeps `graphify-out/graph.html` useful for visitors.

## Interview Explanation

A concise explanation:

```text
After implementing the first five bounded capabilities, I added a public
hardening phase. The goal was to make the repository safe to share, easy to
run through Docker, clear for new readers, and explicit about what Hermes will
not do.
```

That answer shows that the project is not only technical.

It also shows product thinking, safety thinking, and communication.

## Release Checklist

The full release checklist is:

```text
knowledge/36-public-release-checklist.md
```

The LLM decision is:

```text
knowledge/37-llm-private-layer-decision.md
```
