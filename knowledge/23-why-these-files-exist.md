# Why These Files Exist

Hermes is intentionally split into small files because the project has two goals:

- Be useful as a real bounded observability agent.
- Be understandable as an educational open-source architecture.

This note explains why the main files and folders exist.

## Root Files

Root files answer the first questions a visitor usually has.

| File | Purpose |
| --- | --- |
| `README.md` | Explains what Hermes is, how to run it, and where to start. |
| `LICENSE` | Defines how other people can legally use the project. |
| `CONTRIBUTING.md` | Explains how someone can contribute safely. |
| `SECURITY.md` | Explains how to report security issues and what must not be exposed. |
| `CODE_OF_CONDUCT.md` | Sets collaboration expectations for an open-source project. |
| `.env.example` | Shows required configuration keys without exposing real secrets. |
| `.gitignore` | Prevents private files, caches, and local artifacts from being committed. |
| `pyproject.toml` | Defines the Python project metadata, production dependencies, and development dependencies. |
| `Dockerfile` | Builds Hermes as portable runtime and test containers. |
| `docker-compose.demo.yml` | Runs a safe public demo with synthetic data. |
| `docker-compose.test.yml` | Runs the test suite in Docker without requiring host Python setup. |
| `.dockerignore` | Keeps unnecessary or private files out of Docker builds. |

## Knowledge Tree

The `knowledge/` folder is the learning map of Hermes.

It exists because the project is not only code. It also contains architectural decisions, security rules, and the reasoning behind them.

| Area | Files | Purpose |
| --- | --- | --- |
| Vision | `00-vision.md` | Defines why Hermes exists. |
| Public/private model | `01-public-vs-private.md`, `10-open-source-strategy.md` | Explains how the repo can be public while private deployments stay safe. |
| Security | `02-security-boundaries.md`, `07-security.md` | Defines least privilege, secret handling, and forbidden exposure. |
| Architecture | `03-hexagonal-architecture.md`, `06-architecture.md` | Explains the hexagonal design and the role of each layer. |
| Grafana capability | `04-grafana-readonly.md` | Defines the first bounded capability: `grafana.read`. |
| Growth | `05-future-capabilities.md`, `22-capability-matrix.md` | Explains how Hermes can grow without becoming unsafe. |
| Repository orientation | `11-repository-structure.md`, `23-why-these-files-exist.md` | Helps new readers understand the project layout. |
| Roadmap | `30-roadmap-and-learning-path.md` | Explains the order of phases and how to read the project. |
| Public demo hardening | `34-public-demo-hardening.md`, `35-how-to-demo-hermes.md` | Explains how to prepare and present Hermes publicly. |
| Release readiness | `36-public-release-checklist.md`, `37-llm-private-layer-decision.md` | Defines public release gates and why LLM usage stays private and optional. |
| Graph reading | `08-how-to-read-the-graph.md`, `12-graph-reading-index.md` | Explains how to use the generated visual graph. |
| Technical decisions | `13-http-interface-decision.md`, `14-docker-demo.md`, `17-adapter-selection.md`, `18-configuration-model.md` | Records why specific implementation choices were made. |
| Application boundary | `15-application-port-boundary.md`, `16-application-api-adapter.md`, `19-real-application-api-adapter.md`, `20-application-api-contract.md` | Explains why Hermes should talk to a controlled application API. |
| Private inspiration | `21-combinamejor-observability-baseline.md` | Captures the private observability pattern in sanitized public language. |

## Source Code

The `src/hermes/` folder contains the implementation.

It follows hexagonal architecture so the core stays independent from FastAPI, Docker, Grafana, and private infrastructure.

| Folder | Purpose |
| --- | --- |
| `domain/` | Pure concepts such as dashboards, health status, capabilities, and domain errors. |
| `ports/` | Interfaces that describe what Hermes needs, without saying how it is implemented. |
| `application/` | Use cases: the actions Hermes can perform through ports. |
| `infrastructure/` | Adapters that connect ports to real or fake external systems. |
| `interfaces/` | External entry points, currently the HTTP API built with FastAPI. |

## Why There Are Fake Adapters

Fake adapters are not shortcuts.

They are a safety and learning tool.

They allow Hermes to:

- Run without private infrastructure.
- Be demonstrated in public.
- Be tested deterministically.
- Explain the architecture before connecting real systems.

The public repository should work even when no real Grafana, Prometheus, or private application exists.

## Why There Is an Application API Adapter

The application API adapter exists because private deployments should not give Hermes unrestricted infrastructure access.

Preferred private shape:

```text
Hermes -> existing application API -> filtered observability data
```

This lets the existing application own:

- authentication
- authorization
- audit logging
- filtering
- rate limiting
- private infrastructure access

Hermes receives only bounded read-only responses.

## Tests

The `tests/` folder proves that the architecture behaves as intended.

Tests are especially important here because Hermes is designed around boundaries.

They verify:

- use cases call ports correctly
- fake adapters return safe demo data
- configuration rejects invalid sources
- the real-shape application API adapter uses the expected contract
- missing dashboards become domain errors
- the public HTTP API returns the expected read-only responses

The `httpx2` dependency is development-only. It is used by FastAPI/Starlette's `TestClient` to simulate HTTP requests in tests without starting Uvicorn.

## Graphify Output

The `graphify-out/` folder contains generated visual artifacts.

| File | Purpose |
| --- | --- |
| `graph.html` | Interactive graph for visual exploration. |
| `GRAPH_REPORT.md` | Human-readable graph report. |
| `graph.json` | Machine-readable graph data. |
| `manifest.json` | Generation metadata. |
| `cost.json` | Cost/token metadata when available. |

These files help users see how the concepts relate to each other.

## Design Principle

Every file should answer one of these questions:

- What is Hermes?
- What can Hermes do?
- What is Hermes forbidden to do?
- How does Hermes stay safe in public?
- How does Hermes connect privately without leaking details?
- How can a future contributor extend it?

If a new file does not answer one of those questions, it probably does not belong in the project yet.
