# Application API Contract

Hermes should communicate with the existing application through a small read-only contract.

This contract describes the endpoints the existing application can expose for Hermes.

The private observability baseline that motivated this contract is summarized in `knowledge/21-combinamejor-observability-baseline.md`.

## Goal

Hermes should not discover or control private infrastructure directly.

Instead, the existing application exposes selected data through internal endpoints.

```text
Hermes
-> application API contract
-> existing application
-> Grafana/admin data
```

## Required Endpoints

### Health

```text
GET /internal/hermes/grafana/health
```

Expected response:

```json
{
  "service": "application-api",
  "reachable": true,
  "message": "ok"
}
```

### Search Dashboards

```text
GET /internal/hermes/grafana/search
```

Expected response:

```json
[
  {
    "uid": "admin-overview",
    "title": "Admin Overview",
    "url": "/d/admin-overview"
  }
]
```

### Get Dashboard

```text
GET /internal/hermes/grafana/dashboards/{uid}
```

Expected response:

```json
{
  "uid": "admin-overview",
  "title": "Admin Overview",
  "panels": ["Health", "Jobs", "Errors"]
}
```

## Ownership

The existing application owns:

- authentication
- authorization
- validation
- audit trail
- access to Grafana/admin data
- filtering sensitive information

Hermes only consumes the bounded response.

## Error Behavior

If a dashboard is missing, the application should return:

```text
404 Not Found
```

Hermes maps this to:

```text
DashboardNotFound
```

Other failures are treated as application API errors.

## Safety

These endpoints should be internal and read-only.

They should not expose:

- raw tokens
- private infrastructure details
- unfiltered logs
- unrestricted dashboard data
- write operations

## Public Repository

The public repository includes the contract and tests, but no private URL.

The real base URL belongs in:

```text
.env
docker-compose.override.yml
```
