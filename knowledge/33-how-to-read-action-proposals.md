# How To Read Action Proposals

This guide explains how to read the output of:

```text
actions.propose
```

An action proposal is not an executed action.

It is a human-reviewable recommendation.

## Why This Guide Exists

Hermes now follows this path:

```text
metrics.read
-> operations.explain
-> maintenance.plan.generate
-> actions.propose
```

Each step adds more usefulness, but Hermes still stays bounded.

The key difference is:

```text
maintenance plan = ordered work to consider
action proposal = concrete human action to review
```

## Proposal Fields

An action proposal has these fields:

| Field | Meaning |
| --- | --- |
| `title` | Short name of the proposed action. |
| `proposal_type` | Category of proposal, such as capacity review or threshold review. |
| `reason` | Why Hermes thinks the proposal may help. |
| `evidence` | What observed or planned facts support the proposal. |
| `preconditions` | Checks that should be true before acting. |
| `approval_required` | Whether a human must approve before action. |
| `risk` | Risk level of the proposal. |
| `human_action` | What a person should consider doing. |
| `must_not_execute` | Things Hermes must not do automatically. |

## Example: Worker Queue

For the synthetic `worker_queue` signal, Hermes can propose:

```text
Review worker capacity
```

This proposal exists because:

- the worker queue is degraded
- the trend is increasing
- the maintenance plan includes a capacity recommendation

That does not mean Hermes will scale workers.

It means Hermes is saying:

```text
A human should review worker capacity if the queue trend persists.
```

## Evidence

Evidence explains why the proposal exists.

Example:

```text
worker_queue status is degraded
worker_queue trend is increasing
maintenance plan includes a capacity recommendation
```

Evidence should be tied to previous phases.

Hermes should not invent private facts.

## Preconditions

Preconditions are checks that should happen before a proposal becomes action.

Example:

```text
confirm workers are healthy
check for repeated job failures
confirm the queue trend persists
```

This prevents premature action.

It keeps Hermes from jumping from one signal to a production change.

## Approval Required

If a proposal could lead to infrastructure or capacity changes, it should require approval.

Example:

```text
approval_required: true
```

This is a safety feature.

It makes the human control point visible.

## Must Not Execute

The `must_not_execute` field is one of the most important fields.

For worker capacity, Hermes says:

```text
do not restart workers automatically
do not change scaling automatically
do not delete queued messages
```

This proves the capability is a proposal layer, not an execution layer.

## How This Helps In Real Work

In a real private deployment, Hermes could help prepare operational reviews:

- what should be reviewed
- why it matters
- what evidence supports it
- what must be checked first
- what needs approval
- what should never happen automatically

That is useful for maintainability and team communication.

It also keeps the public repository safe because the demo uses synthetic data.

## How To Explain This In An Interview

A good explanation is:

```text
Hermes separates proposals from execution.
It can recommend a human-reviewed action with evidence, preconditions, risk,
approval requirements, and explicit forbidden automatic actions.
This makes the agent useful without giving it uncontrolled production power.
```

That answer shows:

- operational judgment
- safety awareness
- observability understanding
- human approval design
- hexagonal architecture discipline
