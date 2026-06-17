# Configuration Model

Hermes treats configuration as a safety boundary.

Configuration is not only a convenience layer. It decides which adapters and capabilities Hermes is allowed to activate.

## Current Setting

The first validated setting is:

```text
HERMES_GRAFANA_SOURCE
```

Allowed values:

```text
fake_grafana
fake_application_api
```

## Safe Default

If no value is provided, Hermes defaults to:

```text
fake_grafana
```

This is safe for public demos because it uses synthetic data and no private infrastructure.

## Invalid Values

Unsupported values should fail clearly at startup.

Example:

```text
HERMES_GRAFANA_SOURCE=direct_admin_access
```

Hermes should reject this.

The goal is to avoid ambiguous or dangerous configuration.

## Why This Matters

As Hermes grows, configuration may include:

- application API base URL
- timeouts
- read-only tokens
- adapter selection
- enabled capabilities

Before adding private values, Hermes needs a strict configuration model.

## Public And Private

Public files should contain only examples:

```text
.env.example
docker-compose.demo.yml
```

Private values belong in ignored files:

```text
.env
docker-compose.override.yml
```

## Rule

Every configuration value should answer:

- Is it safe by default?
- Is it validated?
- Is the error message clear?
- Could this expose private systems?
- Does this belong in public examples or private local files?
