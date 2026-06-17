# Graph Reading Index

The knowledge graph should be easy to read at a glance.

This file is a human-friendly index for the main community names used in the graph.

## Community Names

### Public And Private Usage

This area explains how Hermes can be public while still supporting private deployments.

Look here for:

- public repository
- private configuration
- private use
- public core
- synthetic demo data

### Capability And Security Path

This area explains the first capability and the safety boundaries around it.

Look here for:

- `grafana.read`
- explicit capabilities
- read-only endpoints
- viewer service account token
- least privilege
- roadmap

### Learning And Code Structure

This area explains how the project is organized for learning and future implementation.

Look here for:

- Hermes Observability Agent
- knowledge graph
- knowledge tree
- repository structure
- future code structure

### Hexagonal Infrastructure

This area explains the architectural core.

Look here for:

- hexagonal architecture
- domain layer
- application layer
- HTTP interface
- infrastructure adapters
- Grafana HTTP API

### Repository Governance

This area explains the open source files that live at the root of the repository.

Look here for:

- root files
- open source governance
- open source quality bar
- license
- contribution and security expectations

## Reading Tip

Start with the largest nodes first.

Then use the community names to understand the neighborhood around each node.

If two communities look close together, that usually means they share an important concept.

Example:

```text
grafana.read
```

connects the capability plan with the security model.

Another example:

```text
Hermes Observability Agent
```

connects the project vision, repository structure, and future implementation.
