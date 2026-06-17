# How To Read Operational Explanations

This guide explains how to read the output of:

```text
operations.explain
```

An operational explanation is not a command.

It is Hermes helping the user understand what a signal might mean.

## Why This Guide Exists

Phase 2 gives Hermes signals.

Phase 3 gives Hermes explanations.

The important difference is:

```text
signal = what Hermes sees
explanation = what Hermes thinks it could mean
```

For example:

```text
worker_queue is degraded and increasing
```

That signal alone is useful, but incomplete.

Hermes then explains:

- what the signal means
- what risk it may represent
- what might be causing it
- what checks are safe
- what actions should not be done automatically

## Explanation Fields

An explanation has these fields:

| Field | Meaning |
| --- | --- |
| `signal` | The operational signal being explained. |
| `meaning` | A human-readable interpretation of the signal. |
| `risk` | What could happen if the signal gets worse or stays unresolved. |
| `possible_causes` | Hypotheses to investigate, not proven root causes. |
| `recommended_checks` | Safe checks a human or approved system can perform. |
| `safe_actions` | Low-risk actions such as documenting, reviewing, or inspecting through approved boundaries. |
| `unsafe_actions` | Things Hermes must not do automatically. |
| `confidence` | How confident Hermes is in this explanation. |

## Example: Worker Queue

The synthetic public demo includes this signal:

```json
{
  "name": "worker_queue",
  "status": "degraded",
  "severity": "warning",
  "summary": "Queue depth is increasing slowly in the synthetic scenario.",
  "trend": "increasing"
}
```

Hermes can explain it like this:

```text
Jobs are waiting longer before being processed.
```

That means the application may still work, but some background tasks could be delayed.

Examples of background work could be:

- emails
- reports
- imports
- notifications
- asynchronous processing

The public demo does not expose real private workers.

It only teaches the reading pattern.

## Possible Causes Are Not Proof

This is one of the most important ideas.

When Hermes says:

```text
workers are slower than incoming jobs
jobs are failing and retrying
one worker group is stopped
```

Hermes is not proving that one of those things happened.

Hermes is saying:

```text
These are reasonable directions to investigate.
```

That is how observability is normally read.

You move from signal to hypothesis, then from hypothesis to evidence.

## Recommended Checks

Recommended checks are the next safe questions.

For `worker_queue`, Hermes may recommend:

```text
check worker health
compare queue trend over the last few minutes
look for repeated job failures
check whether a deployment happened recently
```

These checks are useful because they narrow the problem without changing the system.

This is why Phase 3 stays safe.

Hermes explains and guides.

Hermes does not execute remediation.

## Safe Actions

Safe actions are actions with low operational risk.

Examples:

```text
document the observation
inspect worker logs through the approved application boundary
review whether worker capacity is enough
```

These actions still depend on the private environment.

In the public repository, they remain educational and synthetic.

In a private deployment, they should go through the existing application boundary.

## Unsafe Actions

Unsafe actions are explicitly forbidden for Hermes.

Examples:

```text
delete queued messages without analysis
restart production automatically
change infrastructure from Hermes without approval
```

This section is important because it proves Hermes is bounded.

It can help with operations without becoming an uncontrolled automation agent.

## Confidence

The `confidence` field tells how specific the explanation is.

Common values:

| Confidence | Meaning |
| --- | --- |
| `high` | Hermes has a specific rule for this signal. |
| `medium` | Hermes has partial context but needs more evidence. |
| `low` | Hermes does not know enough and should stay cautious. |

In the public demo, the known synthetic signals usually have `high` confidence because they are intentionally defined.

In real systems, confidence should be treated carefully.

High confidence still does not mean Hermes should execute changes.

## How This Connects To Phase 4

Phase 3 explains one or more signals.

Phase 4 turns those explanations into a maintenance plan.

The path is:

```text
metrics.read
-> operations.explain
-> maintenance.plan.generate
```

That means Hermes first learns to read, then explain, then organize safe work.

It does not jump directly to execution.

## How To Explain This In An Interview

A good explanation is:

```text
Hermes separates signals from explanations.
A signal tells what was observed, while an explanation describes meaning,
risk, possible causes, safe checks, unsafe actions, and confidence.
This keeps the agent useful for observability while avoiding automatic
production changes.
```

That answer shows:

- observability reasoning
- operational caution
- human approval awareness
- safe agent design
- clear architecture boundaries
