# Docker First Workflow

Hermes should be usable without installing Python dependencies directly on the host machine.

Docker is the primary workflow.

The Hermes HTTP application is guarded by `HERMES_CONTAINER_RUNTIME=docker`.

The official Docker images set this value. If someone tries to start the HTTP app outside the Docker workflow, Hermes fails fast with an explicit error.

## Why Docker First

Hermes is intended to be public, reproducible, and easy to review.

Docker first helps because:

- contributors do not need to match the author's Python setup
- tests can run in a predictable container
- the demo uses the same container shape as future deployments
- private configuration stays outside the image
- CI can reuse the same commands later
- users can validate the project without installing dependencies on the host

## Workflows

### Test

```bash
docker compose -f docker-compose.test.yml run --rm hermes-test
```

This builds the `test` target from the Dockerfile and runs:

```text
python -m unittest discover -s tests
```

### Demo

```bash
docker compose -f docker-compose.demo.yml up --build
```

This builds the `runtime` target from the Dockerfile and starts Hermes on port `8790`.

## Dockerfile Targets

The Dockerfile has two targets:

| Target | Purpose |
| --- | --- |
| `runtime` | Installs production dependencies and runs Hermes. |
| `test` | Installs development dependencies and runs the test suite. |

This keeps runtime dependencies smaller while still making tests reproducible.

The public path should always work through Docker.

## Rule

When adding a new dependency, decide whether it belongs to:

- runtime dependencies
- development/test dependencies
- private deployment configuration

Runtime dependencies must be needed to run Hermes.

Development dependencies must be needed only to test or build Hermes.

Private configuration must never be baked into the Docker image.

The public runtime rule is:

```text
No Docker runtime marker, no Hermes HTTP service.
```
