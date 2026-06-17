# Public Release Checklist

This checklist defines what must be true before Hermes is shared as a public repository.

The goal is to make the public project safe, understandable, and reproducible.

## Release Rule

Hermes can be public only if it is:

- safe by default
- Docker-first
- synthetic-data based
- free of secrets
- free of private infrastructure details
- useful without an LLM API key
- explicit about what it will not execute

## 1. Docker Works

Before release, run:

```bash
docker compose -f docker-compose.test.yml run --rm hermes-test
```

Expected result:

```text
OK
```

Then run:

```bash
docker compose -f docker-compose.demo.yml up --build
```

Expected result:

- Hermes starts on port `8790`
- `/docs` opens
- `/health` returns a healthy response
- demo endpoints return synthetic data

Stop the demo after checking:

```bash
docker compose -f docker-compose.demo.yml down
```

## 2. Public Demo Is Synthetic

The public demo must use:

- fake Grafana data
- fake metric signals
- deterministic explanations
- deterministic maintenance plans
- deterministic action proposals

It must not require:

- a real Grafana instance
- a real Prometheus instance
- a real application endpoint
- a real token
- an LLM API key

## 3. No Secrets

The repository must not contain:

- real service account tokens
- API keys
- passwords
- private base URLs
- production IPs
- real `.env` files
- private docker overrides

Allowed public files:

```text
.env.example
docker-compose.demo.yml
docker-compose.test.yml
```

The example environment file may contain placeholders only.

## 4. No Private Data

The repository must not contain:

- customer data
- real logs
- real screenshots
- raw production metrics
- private dashboard exports
- private infrastructure names
- private incident details

Private reality may inspire public abstractions, but it must stay sanitized.

## 5. README Is Clear

The README should answer these questions quickly:

- What is Hermes?
- What can Hermes do?
- What does Hermes refuse to do?
- How do I run it?
- How do I test it?
- Why is it safe to run publicly?
- Where should I start reading?

The first two minutes matter.

If a visitor cannot understand the boundary quickly, the release is not ready.

## 6. Implemented Capabilities Are Accurate

The capability matrix must match the code.

Currently implemented:

```text
grafana.read
metrics.read
operations.explain
maintenance.plan.generate
actions.propose
```

Still forbidden:

```text
actions.execute
infrastructure mutation
automatic remediation
unrestricted raw data access
```

## 7. LLM Is Private Optional

The public repository must not require an LLM provider.

The public behavior should remain deterministic.

LLM usage belongs to a future private layer where:

- secrets stay outside Git
- prompts can include private context safely
- outputs can be reviewed
- audit and approval rules exist
- deterministic fallbacks remain available

The architecture decision is documented in:

```text
knowledge/37-llm-private-layer-decision.md
```

## 8. Graph Is Current

Before release, refresh:

```text
graphify-out/graph.html
graphify-out/graph.json
graphify-out/GRAPH_REPORT.md
```

The graph should include:

- implemented capabilities
- public demo hardening
- how to demo Hermes
- no execution boundary
- Docker-first workflow
- private LLM decision

If no LLM API key is available for Graphify, a deterministic graph refresh is acceptable as long as it is clearly documented.

## 9. Governance Files Exist

The public repository should include:

```text
LICENSE
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
```

These files help the project look and behave like a real open-source project.

## 10. Final Release Gate

Hermes is ready to publish when all of these are true:

- [ ] Docker tests pass
- [ ] Docker demo starts
- [ ] README is clear
- [ ] knowledge tree is current
- [ ] graph is current
- [ ] no secrets are present
- [ ] no private data is present
- [ ] no execution endpoints exist
- [ ] LLM is not required publicly
- [ ] public/private boundary is documented

## Interview Explanation

A concise explanation:

```text
Before publishing Hermes, I created a public release checklist.
It verifies Docker reproducibility, synthetic demo data, no secrets, no private
data, accurate capability documentation, no execution endpoints, and a clear
decision that LLM usage belongs to the private optional layer.
```

That answer shows professional release thinking, not only coding.
