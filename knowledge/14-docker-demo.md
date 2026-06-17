# Docker Demo

Hermes should be easy to run without private infrastructure.

The Docker demo exists so anyone can start Hermes locally and inspect the API without needing a real Grafana instance or a real token.

## Files

```text
Dockerfile
docker-compose.demo.yml
docker-compose.test.yml
.dockerignore
```

## Why Docker

Docker gives Hermes a reproducible runtime.

This helps:

- contributors run the project quickly
- reviewers test the API without configuring Python manually
- tests run in the same containerized project shape
- future private deployments reuse the same container shape
- the public demo stay separate from private configuration

Docker is the primary workflow for Hermes.

The public workflow should not require installing Python dependencies directly on the host machine.

The Hermes HTTP service checks for the Docker runtime marker set by the Dockerfile:

```text
HERMES_CONTAINER_RUNTIME=docker
```

If that marker is missing, the HTTP app refuses to start.

## Why A Demo Compose File

The compose files are intentionally separate:

```text
docker-compose.demo.yml
docker-compose.test.yml
```

This avoids mixing public demo behavior, test behavior, and private local overrides.

Private deployments can use:

```text
docker-compose.override.yml
```

That file is ignored by Git.

## Current Demo Behavior

The current Docker demo uses the fake Grafana adapter.

This means:

- no real Grafana URL is required
- no token is required
- no private dashboard is exposed
- the API shape can still be tested

## Demo Endpoints

```text
GET /health
GET /api/grafana/search
GET /api/grafana/dashboards/demo-system-overview
```

## Test Command

Run tests through Docker:

```bash
docker compose -f docker-compose.test.yml run --rm hermes-test
```

The test image installs test-only dependencies inside Docker and runs:

```text
python -m unittest discover -s tests
```

This means users do not need a local Python environment to validate Hermes.

## Port

Hermes listens inside the container on:

```text
8790
```

The host port can be changed through:

```text
HERMES_PORT
```

Example:

```bash
HERMES_PORT=8890 docker compose -f docker-compose.demo.yml up --build
```

## Safety Rule

The Docker demo must stay public-safe.

It should use only:

- fake adapters
- synthetic data
- example configuration

It must not include:

- real tokens
- private Grafana URLs
- private dashboards
- production logs
