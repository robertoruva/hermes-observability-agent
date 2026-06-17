# Public Demo

The public demo should prove the architecture without exposing private systems.

## Demo Goal

Show that Hermes can read Grafana-like observability data through a limited capability.

## Demo Data

The demo should use synthetic dashboards and fake metrics.

Examples:

```text
demo-system-overview
demo-api-latency
demo-worker-health
```

## Expected Flow

Future demo command:

```bash
docker compose -f docker-compose.demo.yml up --build
```

Then:

```bash
curl http://localhost:8790/health
curl http://localhost:8790/api/grafana/search
```

## Private Use

Private use should reuse the same code but provide real values through `.env`.

Those values must not be committed.
