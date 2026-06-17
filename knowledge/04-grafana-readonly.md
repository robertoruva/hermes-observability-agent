# Grafana Read-Only Capability

The first Hermes capability is:

```text
grafana.read
```

This capability lets Hermes read information from Grafana without modifying it.

## Planned Operations

Hermes should support:

- checking Grafana connectivity
- searching dashboards
- reading a dashboard by UID

## Why Start Here

This is a good first capability because it is useful, common in companies, and naturally bounded.

It teaches:

- API authentication
- service account permissions
- HTTP client design
- DTO mapping
- application use cases
- read-only security design

## Safe Demo Strategy

The public demo should use local Grafana with synthetic dashboards and fake metrics.

The private setup can point the same Hermes code to a real Grafana URL through `.env`, but those values must never be committed.
