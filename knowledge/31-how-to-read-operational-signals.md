# How To Read Operational Signals

This guide explains how to read the synthetic operational signals exposed by Hermes.

These examples are public demo data.

They are not real production readings.

## Where The Signals Come From

The current public demo uses:

```text
FakeMetricsReader
```

That means the signals are intentionally synthetic.

They exist to teach the shape of operational reading without exposing private infrastructure.

Current endpoints:

```text
GET /api/metrics/summary
GET /api/metrics/signals
```

## Signal Shape

Each signal has:

```text
name
status
severity
summary
trend
```

Example:

```json
{
  "name": "worker_queue",
  "status": "degraded",
  "severity": "warning",
  "summary": "Queue depth is increasing slowly in the synthetic scenario.",
  "trend": "increasing"
}
```

## How To Read Status

| Status | Meaning |
| --- | --- |
| `healthy` | The signal looks normal. |
| `degraded` | The system still works, but something is not optimal. |
| `unavailable` | The signal indicates a component is not reachable or not working. |
| `unknown` | Hermes does not have enough information. |

Important:

```text
degraded does not mean down.
```

It means:

```text
working, but with a warning sign.
```

## How To Read Severity

| Severity | Meaning |
| --- | --- |
| `info` | Informational; usually no action required. |
| `warning` | Needs attention if it persists or worsens. |
| `critical` | High-priority signal that may require urgent review. |

Severity helps prioritize.

Status describes condition.

Trend describes movement.

## How To Read Trend

| Trend | Meaning |
| --- | --- |
| `stable` | The signal is not moving in a worrying direction. |
| `increasing` | The measured condition is growing. This can be good or bad depending on the signal. |
| `decreasing` | The measured condition is falling. This can be good or bad depending on the signal. |
| `unknown` | Hermes cannot infer movement. |

Example:

```text
worker_queue + increasing = more jobs are waiting
```

That may be concerning.

But:

```text
successful_requests + increasing = traffic may be growing
```

That may be positive.

Trend must always be read with the signal name.

## Current Demo Signals

### database

```text
status: healthy
severity: info
trend: stable
```

Meaning:

```text
The synthetic database signal is reachable.
```

How to read it:

- This is a basic health signal.
- It suggests the application can reach its database.
- In a real system, this would not prove the database is fast or healthy under load.

Do not conclude:

- that queries are optimized
- that storage is healthy
- that connection pools are correctly sized

### api_latency

```text
status: healthy
severity: info
trend: stable
```

Meaning:

```text
The synthetic API latency signal is stable.
```

How to read it:

- Latency measures how long responses take.
- Stable latency usually means users are not seeing sudden slowdowns.
- In a real system, percentiles matter: p50, p95, and p99 tell different stories.

Do not conclude:

- that every request is fast
- that all endpoints behave the same
- that mobile users see the same latency as backend checks

### worker_queue

```text
status: degraded
severity: warning
trend: increasing
```

Meaning:

```text
The synthetic queue is still working, but it is accumulating work.
```

How to read it:

- This is not automatically an incident.
- It is a sign to inspect.
- If it continues increasing, background work may become delayed.

Possible real-world causes:

- workers are slower than incoming jobs
- a worker group stopped
- a job type became slower
- jobs are failing and retrying
- traffic increased

Recommended checks:

- Are workers running?
- Are consumers connected?
- Are there repeated job failures?
- Is the queue trend temporary or persistent?
- Did a deployment happen recently?

Do not do immediately:

- delete queued messages
- restart production blindly
- scale workers without checking why the queue is growing

### scrape_targets

```text
status: healthy
severity: info
trend: stable
```

Meaning:

```text
The synthetic monitoring targets are reachable.
```

How to read it:

- In Prometheus terms, a scrape target is something Prometheus reads.
- If targets are healthy, Prometheus can collect metrics.
- If a target is down, Grafana may show missing or stale data.

Do not conclude:

- that the service itself is healthy
- that all useful metrics exist
- that dashboards are complete

A scrape target being up means:

```text
Prometheus can read it.
```

It does not always mean:

```text
the business feature is working.
```

## Reading Order

When looking at operational signals, read in this order:

1. Check status.
2. Check severity.
3. Check trend.
4. Read the summary.
5. Ask what the signal does not prove.
6. Decide the safest next check.

Example:

```text
worker_queue
-> degraded
-> warning
-> increasing
-> queue is growing
-> not proof of outage
-> check workers and job failures
```

## Real Versus Synthetic

The public demo uses fake signals.

That is intentional.

| Public Demo | Private Deployment |
| --- | --- |
| Synthetic values | Real operational values |
| Fake adapter | Application API adapter |
| Safe for GitHub | Private configuration |
| Learning-oriented | Production-oriented |

The shape can stay the same.

The data source changes.

## How This Connects To Grafana

Grafana panels often show values like:

- service up/down
- queue depth
- memory usage
- latency
- scrape target status
- error rate

Hermes turns those ideas into normalized operational signals.

That makes it easier to explain:

```text
what the signal means
what risk it suggests
what to check next
```

This prepares the next phase:

```text
operations.explain
```

## Interview Explanation

A useful explanation:

```text
I read operational signals by separating status, severity, and trend.
Status tells me the current condition, severity tells me priority,
and trend tells me whether the situation is improving or getting worse.
I avoid jumping from one signal to a root cause.
First I identify what the signal proves, what it does not prove, and what I should check next.
```

That is the mindset Hermes is designed to support.
