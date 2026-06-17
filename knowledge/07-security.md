# Security

Hermes is designed around least privilege.

The public repository must be safe to share, and private configuration must stay outside Git.

## Secret Handling

Real secrets belong in:

```text
.env
```

The repository only includes:

```text
.env.example
```

## Grafana Permissions

The Grafana integration should use a service account token with Viewer permissions.

Hermes should not use admin credentials for read-only operations.

## Public Demo Data

Public demos should use synthetic dashboards and fake metrics.

Do not publish real screenshots, real logs, real infrastructure names, or real production dashboard exports.

## Defense In Depth

Hermes should limit access through:

- read-only Grafana credentials
- read-only HTTP endpoints
- explicit capabilities
- ignored private configuration files
- synthetic public demo data
