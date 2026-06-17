# Security Boundaries

Read-only access is safer than admin access, but it is not automatically harmless.

Observability data can reveal sensitive information even when nobody can modify the system.

## Risks In Read-Only Data

Grafana dashboards can expose:

- internal service names
- private URLs
- IP addresses
- error messages
- customer identifiers
- traffic volume
- infrastructure topology
- incident history
- database names
- cost or business metrics

## Three Layers Of Protection

Hermes should limit risk at three levels.

### 1. Credential Scope

Use a Grafana service account token with Viewer permissions.

If the token cannot write, Grafana itself blocks write operations.

### 2. Application Scope

Hermes should expose only read endpoints for the first version.

Allowed:

```text
GET /health
GET /api/grafana/search
GET /api/grafana/dashboards/{uid}
```

Not included:

```text
POST
PUT
PATCH
DELETE
```

### 3. Repository Scope

The public repository should contain only synthetic demo data and safe examples.

Real configuration belongs in ignored local files.
