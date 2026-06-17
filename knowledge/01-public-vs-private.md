# Public vs Private

Hermes should be safe to show publicly.

That means the public repository can contain architecture, code, tests, documentation, and synthetic demo data. It must not contain anything from a real private environment.

## Public Repository

Allowed:

- generic source code
- Docker files for demo use
- `.env.example`
- synthetic dashboards
- fake metrics
- architecture documentation
- tests

Not allowed:

- real tokens
- private Grafana URLs
- internal IP addresses
- customer data
- production screenshots
- real logs
- private service names if they reveal infrastructure

## Private Configuration

Private deployment details should live in ignored local files:

```text
.env
docker-compose.override.yml
```

This lets the same public code run against a private Grafana instance without exposing secrets.

## Interview Explanation

Hermes is designed so the public repo demonstrates the architecture and engineering approach, while real credentials and private infrastructure details are injected through local configuration that is not committed.
