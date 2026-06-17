# Adapter Selection

Hermes can choose which read adapter to use through configuration.

This keeps the core stable while allowing different public and private shapes.

## Configuration

The current setting is:

```text
HERMES_GRAFANA_SOURCE
```

Supported demo values:

```text
fake_grafana
fake_application_api
```

## Why This Matters

The use cases do not care where data comes from.

They depend on:

```text
GrafanaReader
```

The configured adapter provides the implementation.

```text
SearchDashboards
-> GrafanaReader
-> FakeGrafanaReader
```

or:

```text
SearchDashboards
-> GrafanaReader
-> FakeApplicationGrafanaReader
```

The use case is unchanged.

## Public Demo

The default public demo uses:

```text
HERMES_GRAFANA_SOURCE=fake_grafana
```

This demonstrates the Grafana capability without real infrastructure.

## Private Direction

For private use, the intended direction is:

```text
HERMES_GRAFANA_SOURCE=application_api
```

That future adapter would call the existing application boundary.

The public repository currently includes only a fake version:

```text
fake_application_api
```

## Safety

Adapter selection should never require committing private URLs or tokens.

Real values belong in:

```text
.env
docker-compose.override.yml
```
