# Roadmap And Learning Path

This guide explains how to read Hermes as a project.

Hermes is not just a set of endpoints.

Hermes is a bounded operational agent that grows through explicit capabilities.

## The Big Idea

Hermes follows this progression:

```text
read
-> understand
-> explain
-> plan
-> propose
-> wait for approval
```

The project intentionally avoids jumping directly to automation.

That is the safety model.

## Current Status

| Phase | Capability | Status | Meaning |
| --- | --- | --- | --- |
| 1 | `grafana.read` | Implemented | Hermes can read safe Grafana-style dashboard data. |
| 2 | `metrics.read` | Implemented | Hermes reads safe synthetic operational signals. |
| 3 | `operations.explain` | Implemented | Hermes explains synthetic operational signals. |
| 4 | `maintenance.plan.generate` | Implemented | Hermes turns explanations into advisory maintenance plans. |
| 5 | `actions.propose` | Implemented | Hermes proposes human-reviewable actions. |

Phases 1 to 5 are implemented right now.

Execution is still intentionally out of scope.

This avoids building unsafe automation by accident.

## Recommended Reading Order

Start here:

```text
knowledge/00-vision.md
knowledge/23-why-these-files-exist.md
knowledge/22-capability-matrix.md
```

Then read the phases:

```text
knowledge/24-phase-1-grafana-read.md
knowledge/26-phase-2-metrics-read.md
knowledge/31-how-to-read-operational-signals.md
knowledge/27-phase-3-operations-explain.md
knowledge/32-how-to-read-operational-explanations.md
knowledge/28-phase-4-maintenance-plan-generate.md
knowledge/29-phase-5-actions-propose.md
knowledge/33-how-to-read-action-proposals.md
knowledge/34-public-demo-hardening.md
knowledge/35-how-to-demo-hermes.md
knowledge/36-public-release-checklist.md
knowledge/37-llm-private-layer-decision.md
```

Then read the Docker and security notes:

```text
knowledge/25-docker-first-workflow.md
knowledge/07-security.md
knowledge/20-application-api-contract.md
knowledge/21-combinamejor-observability-baseline.md
```

## Why The Roadmap Starts With Grafana

Grafana is a familiar operational surface.

Many teams use it to inspect infrastructure, applications, queues, metrics, dashboards, and alerts.

Starting with `grafana.read` lets Hermes prove:

- it can read operational context
- it can stay read-only
- it can avoid private data in public demos
- it can use hexagonal architecture cleanly
- it can run through Docker

## Why Metrics Come Next

Grafana shows panels.

Metrics provide the signals behind those panels.

Phase 2, `metrics.read`, should not expose Prometheus directly.

Instead, Hermes should read safe operational summaries like:

- database reachable
- API latency stable
- worker queue increasing
- scrape target unavailable
- memory usage rising

This gives Hermes useful input without exposing raw monitoring data.

The practical reading guide is:

```text
knowledge/31-how-to-read-operational-signals.md
```

## Why Explanation Comes Before Planning

Hermes should not produce plans before it can explain what it is seeing.

The order matters:

```text
signal
-> meaning
-> risk
-> possible causes
-> recommended checks
```

That is the purpose of `operations.explain`.

It helps users learn how to read observability systems.

## Why Planning Comes Before Proposals

A maintenance plan organizes work.

An action proposal makes one step concrete.

Hermes should first create a plan:

```text
check worker health
review queue trend
document runbook
prepare capacity recommendation
```

Then it can propose a specific human-reviewed action:

```text
Review worker capacity if queue growth continues.
```

This separation keeps Hermes understandable.

## Why Proposals Still Do Not Execute

The practical proposal guide is:

```text
knowledge/33-how-to-read-action-proposals.md
```

An action proposal should include:

- evidence
- preconditions
- risk
- approval requirements
- a human action
- forbidden automatic actions

This lets Hermes become useful without becoming uncontrolled automation.

## Why Explanation Needs A Reading Guide

The practical explanation guide is:

```text
knowledge/32-how-to-read-operational-explanations.md
```

It teaches the difference between:

- a signal
- an explanation
- a possible cause
- a safe check
- an unsafe action
- a confidence level

This matters because Hermes should never treat a hypothesis as proven evidence.

## What Hermes Does Not Do

Hermes does not currently:

- execute commands
- restart services
- scale workers
- edit infrastructure
- silence alerts
- delete data
- mutate Grafana dashboards
- expose raw Prometheus data
- expose private logs

These are intentional boundaries, not missing features.

## Docker First

Hermes is Docker-first.

The supported workflows are:

```bash
docker compose -f docker-compose.test.yml run --rm hermes-test
docker compose -f docker-compose.demo.yml up --build
```

The HTTP service checks for the Docker runtime marker:

```text
HERMES_CONTAINER_RUNTIME=docker
```

This gives users a reproducible and predictable way to run the project.

## Public Versus Private

The public repository contains:

- reusable architecture
- synthetic data
- fake adapters
- tests
- public-safe docs
- capability boundaries
- deterministic behavior without requiring an LLM key

Private deployments provide:

- real URLs
- real tokens
- real dashboards
- real application API endpoints
- environment-specific configuration
- optional LLM behavior after safety boundaries are defined

Private values must stay outside Git.

## Why The LLM Is Private Optional

The LLM decision is documented in:

```text
knowledge/37-llm-private-layer-decision.md
```

The public repository should remain useful without provider accounts, API keys, or token costs.

That keeps Hermes easy to run and safe to inspect.

Private deployments can add an LLM later, but only after:

- authentication
- filtering
- approval
- audit
- deterministic fallbacks

The LLM should amplify Hermes.

It should not become Hermes's security boundary.

## How To Explain This In An Interview

A concise explanation:

```text
Hermes is a Docker-first bounded observability agent.
It starts with read-only Grafana access, then grows toward safe metric reading,
signal explanation, maintenance planning, and action proposals.
Execution is intentionally out of scope.
The public repo uses synthetic data and fake adapters, while private deployments
inject real configuration through an application API boundary.
```

That answer demonstrates:

- observability understanding
- security awareness
- architecture discipline
- Docker reproducibility
- product thinking
- safe AI/agent boundaries

## Next Implementation Step

The current step is consolidation before adding new power:

```text
public demo hardening
```

Recommended implementation order:

```text
review README from a new-user perspective
add endpoint examples
prepare public repository checklist
add demo guide
document private LLM decision
run Docker tests
refresh knowledge graph
Docker tests
```

After that, the next capability should be chosen deliberately.

## Rule For Future Growth

Every new phase should answer:

- What does Hermes read?
- What does Hermes explain?
- What does Hermes propose?
- What is explicitly forbidden?
- What requires human approval?
- What stays private?
- How is it tested through Docker?

If those answers are unclear, the phase is not ready to implement.
