# First Plan And Proposal Demo

This note captures the second part of the first manual Hermes demo.

It continues from:

```text
GET /api/operations/explanations/worker_queue
```

After Hermes explains the signal, the next question is:

```text
What should I do with this information?
```

Hermes answers that in two steps:

```text
maintenance.plan.generate
-> actions.propose
```

## Endpoints Tested

```text
GET /api/maintenance/plan/worker_queue
GET /api/actions/proposals/worker_queue
```

Both endpoints were tested manually through:

```text
http://localhost:8790/docs
```

## Why These Endpoints Matter

The first endpoint creates an ordered maintenance plan.

The second endpoint turns part of that plan into a concrete human-reviewable proposal.

This completes the first useful Hermes story:

```text
read signal
-> explain signal
-> generate plan
-> propose action
-> wait for human approval
```

Hermes still does not execute infrastructure changes.

## Step 1: Maintenance Plan

Endpoint:

```text
GET /api/maintenance/plan/worker_queue
```

This asks Hermes:

```text
You explained the worker queue signal.
What safe plan should I follow next?
```

The plan is advisory.

It should organize work, not perform work.

## How To Read The Plan

A maintenance plan usually contains:

| Field | Meaning |
| --- | --- |
| `title` | Human-readable name of the plan. |
| `priority` | How important the plan is. |
| `summary` | Why Hermes generated the plan. |
| `steps` | Ordered checks, investigations, documentation tasks, or proposals. |
| `source_signals` | Signals that caused the plan to exist. |
| `requires_approval` | Whether any step needs human approval. |

The most important part is the list of steps.

Those steps should move from low-risk checks toward higher-risk proposals.

Example reading:

```text
First confirm worker health.
Then inspect repeated failures.
Then prepare a capacity recommendation if the trend persists.
```

This order matters.

Hermes should not jump directly from:

```text
queue is degraded
```

to:

```text
scale workers now
```

The plan keeps the reasoning disciplined.

## Step 2: Action Proposal

Endpoint:

```text
GET /api/actions/proposals/worker_queue
```

This asks Hermes:

```text
Given the plan, what concrete action should a human review?
```

The answer is a proposal.

It is not execution.

## How To Read The Proposal

An action proposal usually contains:

| Field | Meaning |
| --- | --- |
| `title` | Name of the proposed action. |
| `proposal_type` | Category of the proposal. |
| `reason` | Why Hermes proposes it. |
| `evidence` | Signals or plan facts that support it. |
| `preconditions` | What must be checked before acting. |
| `approval_required` | Whether a human must approve. |
| `risk` | Risk level of the proposal. |
| `human_action` | What a person should consider doing. |
| `must_not_execute` | Actions Hermes must not perform automatically. |

The most important field is:

```text
approval_required
```

For worker capacity or operational changes, this should be:

```text
true
```

That means Hermes can recommend, but a person must decide.

## Why Approval Matters

Approval is not bureaucracy.

In this project, approval is part of the safety architecture.

It proves that Hermes is bounded:

```text
Hermes can propose a capacity review.
Hermes cannot change scaling automatically.
```

This distinction is very important in real companies.

Teams may want operational assistance, but they usually do not want an unrestricted agent changing production systems.

## What This Demo Proves

This manual test proves that Hermes can:

- receive a request through the HTTP interface
- use a known operational signal
- generate an ordered maintenance plan
- produce a concrete proposal
- include evidence and preconditions
- mark approval requirements
- explicitly list actions it must not execute

It also proves that the public demo remains safe because the data is synthetic.

## How To Explain It In An Interview

A clear explanation is:

```text
After testing the explanation endpoint, I tested the maintenance plan and
action proposal endpoints for the same worker_queue signal.
Hermes generated an ordered plan and then proposed a human-reviewable action.
The proposal included evidence, preconditions, risk, approval requirements,
and explicit actions Hermes must not execute automatically.
This shows the difference between useful operational assistance and unsafe
automation.
```

This shows knowledge of:

- observability workflows
- safe operational decision-making
- human approval boundaries
- risk-aware automation
- API-driven demos
- agent capability design

## Complete First Demo Story

The full story is:

```text
GET /api/metrics/summary
GET /api/operations/explanations/worker_queue
GET /api/maintenance/plan/worker_queue
GET /api/actions/proposals/worker_queue
```

What this means:

```text
Hermes reads a synthetic operational situation.
Hermes explains the degraded worker queue.
Hermes generates a safe maintenance plan.
Hermes proposes a human-reviewed action.
Hermes does not execute the action.
```

That is the first complete public demo.
