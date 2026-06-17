# Hermes Vision

Hermes is a bounded observability agent.

Its purpose is not to become an all-powerful admin tool. Its purpose is to expose carefully selected operational capabilities through a small, understandable, and secure interface.

The first capability is reading Grafana.

## Why This Matters

Grafana is common in companies because it shows the health of systems, infrastructure, applications, and sometimes business metrics.

Being able to connect to Grafana safely demonstrates knowledge of:

- observability
- Docker
- API integration
- permission boundaries
- architecture
- security-aware engineering

## Guiding Principle

Hermes should grow by adding explicit capabilities, not by gaining broad access.

Example:

```text
grafana.read
logs.read
alerts.read
alpha.status.read
reports.generate
```

Each capability should have a clear purpose, a clear boundary, and a clear risk model.
