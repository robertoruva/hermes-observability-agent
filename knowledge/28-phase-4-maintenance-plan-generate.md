# Phase 4: Maintenance Plan Generate

Phase 4 introduces the capability:

```text
maintenance.plan.generate
```

This phase turns safe operational explanations into structured maintenance plans.

Hermes can help a user decide what to review, improve, or document next.

Hermes still must not execute operational actions.

Current status: implemented with a deterministic rule-based planner for synthetic explanations.

## Purpose

The purpose of this phase is to produce an ordered plan.

Hermes should help answer:

- What should I check first?
- What is the likely impact?
- What is safe to do now?
- What should wait for approval?
- What should be documented?
- What would improve maintainability?

Hermes should not:

- restart services
- change configuration
- clear caches
- scale workers
- modify dashboards
- silence alerts
- write to production systems

The plan is advisory.

The human remains in control.

## Relationship To Earlier Phases

The path is:

```text
grafana.read
-> metrics.read
-> operations.explain
-> maintenance.plan.generate
```

Phase 1 reads dashboard metadata.

Phase 2 reads safe operational signals.

Phase 3 explains the meaning and risk of those signals.

Phase 4 groups explanations into a maintainable plan.

## Example Input

Input explanations:

```json
[
  {
    "signal": "worker_queue",
    "risk": "Delayed background work if queue growth continues.",
    "recommended_checks": [
      "check worker health",
      "compare queue trend",
      "look for repeated job failures"
    ]
  },
  {
    "signal": "memory_usage",
    "risk": "A growing memory trend may indicate inefficient processing or a leak.",
    "recommended_checks": [
      "compare memory usage after worker restarts",
      "inspect recent heavy jobs",
      "review long-running processes"
    ]
  }
]
```

Example plan:

```json
{
  "title": "Worker Queue Maintenance Plan",
  "priority": "medium",
  "summary": "Queue growth and memory trend should be reviewed before they affect users.",
  "steps": [
    {
      "order": 1,
      "title": "Confirm worker health",
      "kind": "check",
      "risk": "low",
      "requires_approval": false
    },
    {
      "order": 2,
      "title": "Review repeated job failures",
      "kind": "investigation",
      "risk": "low",
      "requires_approval": false
    },
    {
      "order": 3,
      "title": "Prepare capacity recommendation",
      "kind": "proposal",
      "risk": "medium",
      "requires_approval": true
    }
  ]
}
```

## Plan Rules

Hermes should:

- produce ordered steps
- separate checks from proposals
- identify risk level
- mark anything requiring approval
- include documentation tasks
- keep plans tied to observed signals
- explain uncertainty

Hermes should not:

- generate plans from unsupported data
- recommend destructive changes as automatic steps
- hide approval requirements
- include private infrastructure details in public output
- claim an action was executed

## Domain Concepts

Phase 4 introduces:

```text
MaintenancePlan
MaintenanceStep
MaintenancePriority
StepKind
StepRisk
```

Possible step kinds:

```text
check
investigation
documentation
proposal
follow_up
```

This keeps plans understandable and reviewable.

## Port

The planner can be represented by:

```text
MaintenancePlanner
```

Candidate operation:

```text
generate_plan(explanations)
```

The first implementation should be deterministic and rule-based.

The public demo should not require an external LLM.

## Use Cases

The implemented use cases are:

```text
GenerateMaintenancePlan
GenerateSignalMaintenancePlan
```

The use case can depend on:

```text
MetricsReader
OperationsExplainer
MaintenancePlanner
```

## HTTP Surface

The public Docker demo exposes:

```text
GET /api/maintenance/plan
GET /api/maintenance/plan/{signal_name}
```

These endpoints should return advisory plans only.

They should not trigger execution.

## Public Fake Behavior

The public implementation can generate plans for synthetic scenarios:

- worker queue growing
- memory usage increasing
- scrape target unavailable

The current fake metric set includes:

- database healthy
- API latency stable
- worker queue degraded
- scrape targets healthy

The worker queue signal produces a medium-priority maintenance plan because it is the synthetic scenario with the clearest operational follow-up.

## How To Read A Plan

A maintenance plan has:

| Field | Meaning |
| --- | --- |
| `title` | Human-readable name for the plan. |
| `priority` | Overall urgency of the plan. |
| `summary` | Why the plan exists. |
| `steps` | Ordered maintenance steps. |

Each step has:

| Field | Meaning |
| --- | --- |
| `order` | Execution order for review, not automatic execution. |
| `title` | Short name of the step. |
| `kind` | Type of work: check, investigation, documentation, proposal, or follow-up. |
| `risk` | Operational risk of the step. |
| `requires_approval` | Whether a human must approve before acting on it. |
| `summary` | Why the step exists. |

## Validation Criteria

Phase 4 is considered complete for the public rule-based implementation when:

- [x] `maintenance.plan.generate` appears in the capability matrix
- [x] maintenance domain models exist
- [x] a `MaintenancePlanner` port exists
- [x] use cases depend on ports
- [x] a rule-based adapter returns synthetic plans
- [x] HTTP endpoints expose advisory plans
- [x] steps separate checks, documentation, and proposals
- [x] steps that could lead to infrastructure changes require approval
- [x] Docker tests cover the capability

## Interview Explanation

Hermes does not jump from observability to remediation.

Hermes first reads signals, explains them, and then generates a safe maintenance plan.

The plan can include checks, investigations, documentation tasks, and proposals, but it does not execute those tasks.

This demonstrates operational maturity because Hermes keeps human approval and system boundaries visible.
- database reachable but slow
- dashboard coverage incomplete

The output should teach users how to reason about operational maintenance.

## Maintainability Focus

Plans should include improvement work, not only incident response.

Examples:

- add missing metric
- document an operational runbook
- define an alert threshold
- review dashboard coverage
- add a test for an internal contract
- clarify ownership of a service

This makes Hermes useful even when nothing is currently broken.

## Safety Boundary

`maintenance.plan.generate` is not `actions.execute`.

Hermes can say:

```text
Create a proposal to increase worker capacity if queue growth continues.
```

Hermes must not do:

```text
Increase worker capacity automatically.
```

Execution remains outside scope.

## Validation Criteria

Phase 4 should be considered designed when:

- `maintenance.plan.generate` appears in the capability matrix
- planning is documented as advisory only
- plans separate checks, investigations, documentation, and proposals
- approval requirements are explicit
- plans are tied to safe explanations from `operations.explain`
- Docker tests cover the planner once implemented

## Interview Explanation

Hermes can translate observability signals into maintenance plans.

It helps prioritize checks and improvements, but it does not perform production changes.

This keeps the agent useful, explainable, and safe.
