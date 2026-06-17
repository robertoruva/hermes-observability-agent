# Repository Structure

Hermes should be easy to understand from the root of the repository.

The repository structure should separate four concerns:

- project entry point
- open source governance
- knowledge tree
- implementation code

## Root Files

The root of the repository contains files that people expect to find immediately.

```text
README.md
LICENSE
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
.env.example
.gitignore
```

These files answer first-level questions:

- What is this project?
- Can I use it?
- How do I contribute?
- How do I report security issues?
- What should never be committed?
- How do I configure it safely?

## Knowledge Tree

Conceptual documentation lives in:

```text
knowledge/
```

This is the learning map of Hermes.

For a practical explanation of why the main files and folders exist, see `knowledge/23-why-these-files-exist.md`.

It explains:

- vision
- public vs private boundaries
- security model
- hexagonal architecture
- Grafana read-only capability
- future capabilities
- open source strategy
- repository structure

The knowledge tree is intentionally separate from implementation code.

## Graphify Output

The generated knowledge graph lives in:

```text
graphify-out/
```

Important files:

```text
graphify-out/graph.html
graphify-out/GRAPH_REPORT.md
graphify-out/graph.json
```

These files turn the knowledge tree into a visual map.

They help readers understand how concepts relate to each other.

## Future Code Structure

Implementation will live in:

```text
src/
```

The planned structure follows hexagonal architecture:

```text
src/
  domain/
  application/
  ports/
  infrastructure/
  interfaces/
```

This keeps the core independent from external tools such as Grafana, Docker, or HTTP frameworks.

## Private Local Files

Private files should not be committed.

Examples:

```text
.env
docker-compose.override.yml
```

These files can contain real private configuration for a local or production environment.

They are ignored because Hermes is open source by design but private by configuration.

## Public Demo Files

Future demo files should be safe to publish.

Possible structure:

```text
demo/
  grafana/
  prometheus/
  dashboards/
```

The demo should use synthetic data only.

## Growth Rule

When adding a new file or folder, ask:

- Is this conceptual knowledge?
- Is this source code?
- Is this public demo material?
- Is this private configuration?
- Is this open source governance?

The answer decides where the file belongs.

This rule keeps Hermes understandable as it grows.
