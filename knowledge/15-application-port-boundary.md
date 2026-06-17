# Application Port Boundary

Hermes should not become a second infrastructure platform.

For private use, Hermes should interact with the existing application through a controlled application boundary.

This means Hermes should not directly manage databases, servers, containers, cloud resources, or internal infrastructure unless that access is explicitly exposed by the application through a safe interface.

## Main Principle

Hermes can ask the application to perform or expose bounded actions.

Hermes should not bypass the application.

```text
Hermes
-> controlled application port/API
-> existing application
-> existing infrastructure
```

Not:

```text
Hermes
-> database/server/cloud/infrastructure directly
```

## Why This Matters

This keeps the scope safer.

The existing application remains the owner of:

- business rules
- permissions
- data access
- audit trail
- validation
- infrastructure knowledge

Hermes becomes an orchestrator or reader of bounded capabilities, not an unrestricted operator.

## Admin Panel Use Case

Hermes may eventually help with admin-panel-related workflows.

Examples:

```text
admin.status.read
admin.metrics.read
admin.reports.generate
admin.documentation.search
```

But those capabilities should be exposed through the existing application boundary.

Hermes should not create a separate admin system that competes with or bypasses the main application.

## Grafana Use Case

For Grafana, the first public capability is:

```text
grafana.read
```

In private use, if Grafana is already part of the existing application environment, Hermes should connect through the safest available boundary:

- a read-only Grafana token when direct Grafana API access is acceptable
- an application endpoint that exposes selected Grafana data
- a backend service that already owns observability permissions

The preferred approach depends on where the real permission boundary lives.

## Network Port vs Hexagonal Port

There are two different meanings of "port".

### Network/API Port

This is how Hermes talks to another running system.

Example:

```text
http://localhost:8000/internal/hermes/grafana
```

### Hexagonal Port

This is an interface inside the code.

Example:

```text
GrafanaReader
```

The use case depends on the hexagonal port. The infrastructure adapter decides whether the data comes from Grafana directly, the existing application, or a fake demo.

## Preferred Private Shape

The safest private shape is:

```text
Hermes use case
-> Hermes port
-> adapter for existing application API
-> existing application
-> Grafana/admin data
```

This keeps Hermes reusable and avoids giving it broad infrastructure access.

## Rule

Before giving Hermes a new private capability, ask:

- Can this action go through the existing application?
- Does Hermes need direct infrastructure access, or only a bounded application endpoint?
- Who owns permissions and audit logs?
- Can the public demo represent this with synthetic data?

Default answer:

```text
Use the existing application boundary first.
```
