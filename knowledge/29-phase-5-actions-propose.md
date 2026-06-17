# Phase 5: Actions Propose

Phase 5 introduces the capability:

```text
actions.propose
```

This phase turns maintenance plans into concrete action proposals.

Hermes can say what a human might do next.

Hermes must not execute the action.

Current status: implemented with a deterministic rule-based proposer for synthetic maintenance plans.

## Purpose

The purpose of this phase is to make recommendations more concrete while keeping control with the human operator.

Hermes can propose:

- what action to consider
- why the action may help
- what evidence supports it
- what risk it has
- what approval it needs
- what should be checked before doing it
- what rollback or fallback should exist

Hermes must not:

- run commands
- call mutation endpoints
- restart services
- scale workers
- clear caches
- edit configuration
- delete data
- change Grafana, Prometheus, alerts, or infrastructure

This is a proposal capability, not an execution capability.

## Relationship To Earlier Phases

The path is:

```text
grafana.read
-> metrics.read
-> operations.explain
-> maintenance.plan.generate
-> actions.propose
```

Phase 4 creates a plan.

Phase 5 turns selected plan steps into explicit proposals.

The proposal still waits for human review.

## Example Input

Maintenance plan step:

```json
{
  "order": 3,
  "title": "Prepare capacity recommendation",
  "kind": "proposal",
  "risk": "medium",
  "requires_approval": true
}
```

Example action proposal:

```json
{
  "title": "Review worker capacity for the heavy queue",
  "proposal_type": "capacity_review",
  "reason": "Queue depth is increasing and background work may become delayed.",
  "evidence": [
    "worker_queue trend is increasing",
    "maintenance plan marked capacity review as medium risk"
  ],
  "preconditions": [
    "confirm workers are healthy",
    "check for repeated job failures",
    "confirm the queue trend persists"
  ],
  "approval_required": true,
  "risk": "medium",
  "human_action": "Open an operational review and decide whether worker capacity should be adjusted.",
  "must_not_execute": [
    "do not restart workers automatically",
    "do not change scaling automatically",
    "do not delete queued messages"
  ]
}
```

## Proposal Rules

Hermes should:

- produce proposals in plain language
- explain why the action is being suggested
- include supporting evidence
- show required preconditions
- mark approval requirements clearly
- identify risk level
- include what must not be done automatically
- keep proposals tied to plans and observed signals

Hermes should not:

- output shell commands as the primary recommendation
- hide risk or uncertainty
- make private infrastructure assumptions
- claim that an action was performed
- create proposals from unsupported data
- skip human review for medium or high risk changes

## Domain Concepts

Phase 5 introduces:

```text
ActionProposal
ProposalType
ProposalRisk
```

The domain model should make a proposal clearly different from an executed action.

## Port

The proposal generator can be represented by:

```text
ActionProposer
```

Candidate operation:

```text
propose_actions(maintenance_plan)
```

The first implementation should be deterministic and rule-based.

The public demo should not require an external LLM.

## Use Cases

The implemented use cases are:

```text
ProposeMaintenanceActions
ProposeSignalActions
```

The use case can depend on:

```text
MaintenancePlanner
ActionProposalGenerator
```

## HTTP Surface

The public Docker demo exposes:

```text
GET /api/actions/proposals
GET /api/actions/proposals/{signal_name}
```

These endpoints should return proposals only.

They must not trigger any change.

## Public Fake Behavior

The public implementation can propose safe review actions for synthetic scenarios:

- review worker capacity
- add an alert threshold
- document a runbook
- inspect dashboard coverage
- add a missing metric
- schedule a performance review

The output should help users understand how operational recommendations are formed.

## How To Read Proposals

The practical reading guide is:

```text
knowledge/33-how-to-read-action-proposals.md
```

This guide explains:

- evidence
- preconditions
- risk
- approval requirements
- human action
- forbidden automatic actions

## Safety Boundary

`actions.propose` is not `actions.execute`.

Hermes can say:

```text
Consider reviewing worker capacity if queue growth continues.
```

Hermes must not do:

```text
Scale workers now.
```

Execution should be a separate future capability, if it is ever added.

That future capability would require:

- explicit user approval
- strong authentication
- authorization rules
- audit logging
- dry-run support
- rollback planning
- environment restrictions
- much stricter tests

## Why This Matters Professionally

Many companies are interested in operational automation, but unsafe automation creates risk.

This phase demonstrates a mature boundary:

```text
observe
-> explain
-> plan
-> propose
-> wait for approval
```

That is easier to trust than an agent that immediately changes production.

## Validation Criteria

Phase 5 is considered complete for the public rule-based implementation when:

- [x] `actions.propose` appears in the capability matrix
- [x] action proposals are clearly separated from execution
- [x] proposals include evidence, preconditions, risk, and approval requirements
- [x] public examples use synthetic data
- [x] Docker tests cover proposal generation
- [x] no proposal endpoint performs mutations

## Interview Explanation

Hermes can propose operational actions, but it does not execute them.

This keeps recommendations useful while preserving human control, auditability, and safety.
