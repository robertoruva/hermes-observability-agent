# External User Review

This note captures a first external-user style review of the public repository.

The purpose is to check whether someone can start from GitHub, clone the project, run Docker, and understand the demo without private context.

## Review Date

```text
2026-06-23
```

## Review Method

The repository was cloned into a temporary directory outside the working copy.

That matters because it simulates a new user starting from the public GitHub repository.

The review used:

```bash
git clone https://github.com/robertoruva/hermes-observability-agent.git
cd hermes-observability-agent
docker compose -f docker-compose.demo.yml up --build -d
```

## Results

| Check | Result | Notes |
| --- | --- | --- |
| Public clone works | Pass | The repository cloned from GitHub successfully. |
| Docker build works | Pass | The image built from the public Dockerfile. |
| Demo container starts | Pass | The Hermes container started successfully. |
| Container healthcheck works | Pass | Docker reported the container as healthy. |
| Hermes responds inside container | Pass | `/health` and action proposals responded from inside the container. |
| Public fake source is active | Pass | `/health` reported `fake_grafana`. |
| No private configuration required | Pass | The demo did not need real Grafana URLs, tokens, or private files. |
| Host `localhost` access | Needs environment check | Docker published `0.0.0.0:8790->8790`, but this shell could not reach `localhost:8790` during the review. |

## Verified Responses

The health endpoint responded from inside the container:

```json
{
  "service": "grafana",
  "reachable": true,
  "message": "Fake Grafana reader is available.",
  "source": "fake_grafana"
}
```

The action proposal endpoint also responded:

```text
GET /api/actions/proposals/worker_queue
```

It returned proposals including:

```text
Review worker capacity
Document queue review threshold
```

The response included:

- evidence
- preconditions
- approval requirements
- risk
- human action
- actions Hermes must not execute automatically

## Important Finding

The application worked inside Docker.

Docker also reported the port mapping:

```text
0.0.0.0:8790->8790/tcp
```

However, the terminal environment used for this review could not reach:

```text
http://localhost:8790
```

This appears to be an environment-level Docker Desktop or host-port access issue, not a Hermes application failure.

For a normal user, the expected manual check remains:

```text
http://localhost:8790/docs
```

If that does not open, the user should check:

- Docker Desktop is fully running
- no other service is using port `8790`
- Docker has permission to expose ports to the host
- the container is healthy with `docker compose -f docker-compose.demo.yml ps`

## What This Review Proves

This review proves that the public repository is close to the intended external-user shape:

```text
clone
-> build Docker image
-> start Hermes
-> use fake public data
-> inspect bounded proposals
```

The public demo does not require:

- local Python installation
- real Grafana access
- production tokens
- private dashboards
- private application URLs
- LLM API keys

## Remaining Public Polish

Before cutting to the private phase, consider adding a short troubleshooting section to the README:

```text
If Docker starts but http://localhost:8790/docs does not open, check Docker Desktop and port 8790.
```

This would help first-time users distinguish between:

```text
Hermes application failure
```

and:

```text
local Docker host networking issue
```

## Cut Readiness

The public repository is almost ready to act as the stable public base.

The remaining public closure should be:

```text
1. Add README troubleshooting note.
2. Optionally tag the public demo version.
3. Start the private integration plan separately.
```

This keeps the public project safe, useful, and understandable before private configuration enters the picture.
