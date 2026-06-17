# First Manual Demo

This note captures the first manual test of Hermes through the OpenAPI page.

It is intentionally practical.

The goal is to remember not only that Hermes worked, but also how to read what it returned.

## Endpoint Tested

```text
GET /api/operations/explanations/worker_queue
```

This endpoint belongs to:

```text
operations.explain
```

It asks Hermes to explain one operational signal.

In this demo, the signal is:

```text
worker_queue
```

## How The Test Was Run

Hermes was running through Docker.

The manual test was performed from:

```text
http://localhost:8790/docs
```

In the OpenAPI page:

```text
GET /api/operations/explanations/{signal_name}
```

was opened, `Try it out` was selected, and this value was used:

```text
worker_queue
```

Then `Execute` was selected.

## What A Successful Response Means

The response returned:

```text
Code 200
```

That means the request succeeded.

Hermes understood the signal name and returned an operational explanation.

This proves:

- Hermes is running inside Docker
- the HTTP interface is available
- the `operations.explain` use case is connected
- the demo data can be read safely
- Hermes can explain a signal without executing changes

## How To Read The Response

The response contains several important sections.

### Possible Causes

Example values:

```text
workers are slower than incoming jobs
one worker group is stopped
a recent job type is taking longer than expected
jobs are failing and retrying
```

These are hypotheses.

They are not proven root causes.

Hermes is saying:

```text
These are reasonable directions to investigate.
```

This is important because real observability work usually moves from:

```text
signal -> hypothesis -> evidence -> decision
```

Hermes should not jump from one signal directly to an automatic fix.

### Recommended Checks

Example values:

```text
check worker health
compare queue trend over the last few minutes
look for repeated job failures
check whether a deployment happened recently
```

These are safe next questions.

They help narrow the investigation without changing the system.

This is useful because Hermes becomes a guide for operational reasoning.

### Safe Actions

Example values:

```text
document the observation
inspect worker logs through the approved application boundary
review whether worker capacity is enough
```

These are actions with low risk.

In a private deployment, these actions should still go through the approved application boundary.

Hermes should not bypass the application or infrastructure rules.

### Unsafe Actions

Example values:

```text
delete queued messages without analysis
restart production automatically
change infrastructure from Hermes without approval
```

This section is one of the most important parts of the demo.

It shows that Hermes is bounded.

Hermes can help understand an operational issue, but it does not take dangerous action on its own.

## Why This Demo Matters

This small test demonstrates the core value of Hermes:

```text
Hermes does not only return data.
Hermes helps interpret data safely.
```

The endpoint does not just say:

```text
worker_queue is degraded
```

It explains:

- what might be happening
- what should be checked
- what can be done safely
- what must not be done automatically
- how confident the explanation is

That is the difference between a simple monitoring endpoint and an observability assistant.

## How To Explain It In An Interview

A clear explanation is:

```text
I built Hermes as a bounded observability agent.
In the manual demo, I used the operations.explain capability to ask Hermes
about a degraded worker queue.
Hermes returned possible causes, recommended checks, safe actions, unsafe
actions, and confidence.
The important part is that it helps reason about operations without executing
infrastructure changes automatically.
```

This shows knowledge of:

- observability
- operational signals
- safe automation boundaries
- Docker-first execution
- API-driven interaction
- hexagonal architecture

## What To Do Next

After this explanation endpoint, continue with:

```text
GET /api/maintenance/plan/worker_queue
GET /api/actions/proposals/worker_queue
```

That completes the path:

```text
explain -> plan -> propose
```

This is the first full user-facing story of Hermes.
