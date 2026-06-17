# Phase 2: Metrics Read

Phase 2 introduces the next bounded Hermes capability:

```text
metrics.read
```

This phase should let Hermes read safe operational signals without exposing raw private monitoring data.

Current status: implemented with synthetic data through `FakeMetricsReader`.

## Purpose

The purpose of this phase is not to expose Prometheus directly.

The purpose is to give Hermes a small, understandable operational summary.

Hermes can read:

- service health signals
- high-level metric summaries
- trend direction
- operational severity
- short human-readable explanations

Hermes must not read or expose:

- raw Prometheus dumps
- unrestricted PromQL results
- labels that may contain secrets or private identifiers
- customer data
- full logs
- infrastructure credentials
- write or remediation actions

## Why This Phase Comes After Grafana

Phase 1 proves Hermes can read dashboard metadata safely.

Phase 2 moves one level closer to operational meaning.

Grafana shows panels.

Metrics explain what the panels are based on.

The safe path is:

```text
grafana.read
-> metrics.read
-> operations.explain
-> maintenance.plan.generate
```

Hermes should learn to read before it explains, and explain before it proposes actions.

## Public Model

The public model should be generic and synthetic.

Instead of exposing raw metric names, Hermes should expose operational signals.

Example:

```json
{
  "signals": [
    {
      "name": "database",
      "status": "healthy",
      "severity": "info",
      "summary": "Database is reachable.",
      "trend": "stable"
    },
    {
      "name": "worker_queue",
      "status": "degraded",
      "severity": "warning",
      "summary": "Queue depth is increasing slowly.",
      "trend": "increasing"
    }
  ]
}
```

The important idea is:

```text
Hermes reads interpreted signals, not unrestricted raw monitoring data.
```

## Candidate Domain Concepts

Phase 2 should introduce domain concepts like:

```text
OperationalSignal
SignalStatus
SignalSeverity
TrendDirection
MetricsSnapshot
```

These names are intentionally generic.

They should not mention private application names, real metric families, or production infrastructure.

## Candidate Port

The new port should be:

```text
MetricsReader
```

Candidate operations:

```text
read_snapshot()
list_signals()
```

The port should describe what Hermes needs to know, not where the data comes from.

## Candidate Use Cases

Potential use cases:

```text
ReadMetricsSnapshot
ListOperationalSignals
```

These use cases should depend on the `MetricsReader` port.

They should not depend on Prometheus, Grafana, Docker, HTTP, or the private application.

## Candidate HTTP Surface

Phase 2 can expose:

```text
GET /api/metrics/summary
GET /api/metrics/signals
```

These endpoints should return bounded DTOs.

They should not return raw Prometheus text, unrestricted query results, or private labels.

These endpoints are now available in the public Docker demo using synthetic signals.

## Public Fake Adapter

The first implementation should use:

```text
FakeMetricsReader
```

This adapter should return synthetic signals such as:

- database reachable
- API latency stable
- worker queue warning
- scrape targets healthy

The fake adapter lets users learn the shape of Hermes without needing real infrastructure.

## Private Integration Path

Private deployments should still prefer:

```text
Hermes -> existing application API -> filtered operational signals
```

The existing application can translate real observability data into safe Hermes DTOs.

This keeps the application responsible for:

- authentication
- authorization
- filtering
- audit logging
- hiding private infrastructure details

## Relationship To The Private Baseline

The private observability baseline includes:

- application metrics
- database health
- PHP memory usage
- queue signals
- scrape target health
- Grafana dashboards backed by Prometheus

The public `metrics.read` capability should abstract those into generic operational signals.

It should not copy private metric names or production values.

## Validation Criteria

Phase 2 is considered complete for the public fake implementation when:

- [x] `metrics.read` is documented in the capability matrix
- [x] domain models exist for operational signals
- [x] a `MetricsReader` port exists
- [x] use cases depend on the port
- [x] a fake adapter returns synthetic signals
- [x] HTTP endpoints expose safe summaries
- [x] Docker tests cover the capability
- [x] no private metrics or raw monitoring payloads are exposed

## Future Link: Operations Explain

Once `metrics.read` exists, Hermes can start explaining signals.

That future capability can be:

```text
operations.explain
```

Example:

```text
worker_queue is warning
-> possible cause: workers are slower than incoming jobs
-> safe next check: inspect worker health and queue trend
-> unsafe action: deleting messages or restarting production automatically
```

This keeps Hermes useful as a learning assistant and operational advisor while staying bounded.
