# Phase 3: Operations Explain

Phase 3 introduces the capability:

```text
operations.explain
```

This phase turns operational signals into human-readable explanations.

It is designed to help users understand what Grafana, Prometheus, and application metrics are showing without giving Hermes unsafe control over infrastructure.

Current status: implemented with deterministic rule-based explanations for synthetic signals.

## Purpose

The purpose of this phase is not to automate production changes.

The purpose is to explain:

- what a signal means
- why it matters
- what could be causing it
- what to check next
- which actions are safe to consider
- which actions should not be taken automatically

Hermes should behave like an operational tutor and advisor.

It should not behave like an unrestricted production operator.

## Relationship To Earlier Phases

The path is:

```text
grafana.read
-> metrics.read
-> operations.explain
```

Phase 1 reads dashboard metadata.

Phase 2 reads safe operational signals.

Phase 3 explains those signals.

Hermes should not explain signals it has not received through a bounded capability.

## Example Explanation

Input signal:

```json
{
  "name": "worker_queue",
  "status": "degraded",
  "severity": "warning",
  "summary": "Queue depth is increasing slowly.",
  "trend": "increasing"
}
```

Possible Hermes explanation:

```json
{
  "signal": "worker_queue",
  "meaning": "Jobs are waiting longer before being processed.",
  "risk": "If the queue keeps growing, users may experience delayed background work.",
  "possible_causes": [
    "workers are slower than incoming jobs",
    "one worker group is stopped",
    "a recent job type is taking longer than expected"
  ],
  "recommended_checks": [
    "check worker health",
    "compare queue trend over the last few minutes",
    "look for repeated job failures"
  ],
  "safe_actions": [
    "document the incident",
    "inspect worker logs through the approved application boundary",
    "review whether worker capacity is enough"
  ],
  "unsafe_actions": [
    "delete queued messages without analysis",
    "restart production automatically",
    "change infrastructure from Hermes without approval"
  ]
}
```

## Explanation Rules

Hermes should:

- explain in plain language
- connect the signal to operational risk
- show uncertainty when causes are not proven
- recommend safe next checks
- separate observations from assumptions
- avoid exposing private implementation details

Hermes should not:

- invent root causes
- claim certainty without evidence
- expose raw logs or raw metrics
- recommend destructive actions as automatic steps
- execute infrastructure changes
- hide uncertainty from the user

## Candidate Domain Concepts

Phase 3 can introduce:

```text
OperationalExplanation
PossibleCause
RecommendedCheck
SafeAction
UnsafeAction
ExplanationConfidence
```

The domain model should separate:

- observed signal
- interpretation
- possible causes
- next checks
- proposed actions

This separation is important because a signal can suggest several possible causes.

## Candidate Port

Phase 3 may use a port like:

```text
OperationsExplainer
```

Candidate operation:

```text
explain(signal)
```

The first implementation should be deterministic and rule-based.

Hermes should not require an LLM to explain basic operational signals in the public demo.

## Candidate Use Cases

Potential use cases:

```text
ExplainOperationalSignal
ExplainMetricsSnapshot
```

These use cases should depend on:

```text
MetricsReader
OperationsExplainer
```

The use case can read safe signals and then ask the explainer to produce bounded explanations.

## Candidate HTTP Surface

Possible endpoints:

```text
GET /api/operations/explanations
GET /api/operations/explanations/{signal_name}
```

These endpoints should return explanations based on safe signals only.

They should not expose raw monitoring payloads.

These endpoints are now available in the public Docker demo.

## Public Fake Behavior

The public implementation can explain synthetic signals such as:

- database healthy
- API latency stable
- worker queue warning
- scrape target unavailable
- memory usage increasing

This lets users learn how to read operational dashboards without using private production data.

## Teaching Goal

Hermes should help users learn the observability loop:

```text
signal
-> meaning
-> risk
-> possible causes
-> next checks
-> safe recommendations
```

This is useful for interviews and real operations.

A good explanation should help the user answer:

- What am I looking at?
- Why does it matter?
- What would I inspect next?
- What should I avoid doing too early?

## Safety Boundary

`operations.explain` is not `actions.execute`.

Hermes can say:

```text
This queue trend suggests checking worker health.
```

Hermes must not do:

```text
Restart workers automatically.
```

Execution belongs to a future capability and should require explicit approval, audit logging, and a much stricter contract.

## Validation Criteria

Phase 3 is considered complete for the public rule-based implementation when:

- [x] `operations.explain` appears in the capability matrix
- [x] the explanation boundary is documented
- [x] safe and unsafe actions are separated
- [x] explanations are tied to `metrics.read` signals
- [x] the public demo can explain synthetic signals
- [x] Docker tests cover the explanation behavior

## Interview Explanation

Hermes does not replace Grafana.

Hermes adds an interpretation layer over safe observability signals.

It helps users understand operational risk and next checks while keeping execution and remediation out of scope.
