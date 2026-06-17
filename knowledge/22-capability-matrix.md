# Hermes Capability Matrix

This matrix defines what Hermes can do, what it must not do, and how each capability should grow.

The purpose is to keep Hermes explainable, safe, and easy to extend.

## Reading Rule

Each capability should answer four questions:

- What can Hermes read?
- What is explicitly forbidden?
- Which port owns the capability?
- Which adapter can implement it?

If a capability cannot answer those questions, it is not ready to be implemented.

## Current Capability

| Capability | Status | Hermes Can | Hermes Must Not | Port | Current Adapters |
| --- | --- | --- | --- | --- | --- |
| `grafana.read` | Implemented | Check health, search dashboards, read dashboard summaries/details | Create dashboards, edit dashboards, delete dashboards, manage users, manage datasources | `GrafanaReader` | `FakeGrafanaReader`, `FakeApplicationGrafanaReader`, `ApplicationApiGrafanaReader` |

The phase note for this capability is `knowledge/24-phase-1-grafana-read.md`.

## Current Rules

| Rule | Meaning |
| --- | --- |
| Read-only first | Hermes starts by reading operational information only. |
| Application boundary first | Private deployments should prefer the existing application API over direct infrastructure access. |
| Public-safe by default | The repository must run with fake/synthetic data without private configuration. |
| Explicit source selection | The active adapter must be selected by configuration, not hidden in code. |
| Least privilege | Any real token must have the smallest permissions possible. |
| No raw private data | Hermes should not expose raw logs, raw metric dumps, secrets, or customer data. |

## Future Candidate Capabilities

These are possible future capabilities. They are not implemented yet.

| Capability | Status | Hermes Could Read | Forbidden Scope | Preferred Boundary |
| --- | --- | --- | --- | --- |
| `metrics.read` | Implemented | Safe metric summaries, service health, high-level trends | Raw Prometheus dumps, unrestricted PromQL, secrets in labels | `MetricsReader` with fake adapter now; Application API later |
| `operations.explain` | Implemented | Explanations of safe operational signals, possible causes, recommended checks | Invented root causes, automatic remediation, raw private evidence | `OperationsExplainer` with rule-based adapter now; Application API later |
| `maintenance.plan.generate` | Implemented | Advisory maintenance plans from safe explanations | Executing actions, changing infrastructure, hiding approval requirements | `MaintenancePlanner` with rule-based adapter now; Application API later |
| `actions.propose` | Implemented | Human-reviewable action proposals with evidence, preconditions, risk, and approval requirements | Running commands, mutating systems, bypassing approval | `ActionProposer` with rule-based adapter now; Application API later |
| `logs.read` | Candidate | Filtered operational log summaries | Full logs, personal data, credentials, stack traces with secrets | Application API |
| `alerts.read` | Candidate | Active alerts, alert state, alert severity | Editing alert rules, silencing alerts, deleting alerts | Application API |
| `admin.status.read` | Candidate | Admin panel health, worker status, queue pressure | User management, password resets, moderation actions | Application API |
| `incidents.summarize` | Candidate | Summaries built from safe events | Direct remediation, infrastructure writes, private raw evidence | Application API |
| `reports.generate` | Candidate | Generated read-only operational reports | Publishing externally, emailing users, changing state | Application API |

The phase note for `metrics.read` is `knowledge/26-phase-2-metrics-read.md`.

The phase note for `operations.explain` is `knowledge/27-phase-3-operations-explain.md`.

The phase note for `maintenance.plan.generate` is `knowledge/28-phase-4-maintenance-plan-generate.md`.

The phase note for `actions.propose` is `knowledge/29-phase-5-actions-propose.md`.

## Private Example Mapping

The private application can inspire Hermes capabilities without exposing private details.

| Private Reality | Public Hermes Abstraction |
| --- | --- |
| Existing internal metrics endpoint | `metrics.read` candidate |
| Existing Grafana dashboard | `grafana.read` implemented capability |
| Existing Prometheus datasource | Observability datasource |
| Existing admin panel health | `admin.status.read` candidate |
| Existing worker and queue signals | Queue pressure summary |
| Existing production configuration | Private environment variables only |

## Adapter Growth Rule

Every future capability should grow like this:

```text
domain model
-> port
-> use case
-> fake adapter
-> application API adapter
-> HTTP endpoint
-> tests
-> knowledge note
```

This keeps the open-source version useful while keeping the private deployment safe.

## Capability Approval Checklist

Before adding a new capability, answer:

- Is it read-only?
- Can it be demonstrated with synthetic data?
- Does it avoid direct access to private infrastructure?
- Does it avoid exposing user data?
- Does it have a clear port?
- Does it have a fake adapter?
- Does it have tests?
- Is the private configuration outside Git?

If any answer is no, the capability should stay in design until the boundary is clearer.

## Interview Explanation

Hermes is not an unrestricted automation agent.

Hermes is a bounded operational agent with explicit capabilities.

The public repository demonstrates the reusable architecture, while private deployments inject real configuration and use the existing application as the security boundary.
