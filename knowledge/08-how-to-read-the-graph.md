# How To Read The Knowledge Graph

Hermes includes a small knowledge graph to explain the project visually.

The graph is not only decoration. It is a learning tool that shows how the main ideas connect.

Open it here:

```text
graphify-out/graph.html
```

## Nodes

Each circle is a concept.

Examples:

```text
Hermes Observability Agent
grafana.read
Hexagonal Architecture
Viewer Service Account Token
Private Configuration
```

Larger nodes are more connected. They are usually more important for understanding the system.

In the first version of Hermes, the most important nodes are:

```text
Hexagonal Architecture
grafana.read
Ports
Viewer Service Account Token
```

## Arrows

Each arrow is a relationship between two concepts.

Example:

```text
grafana.read -> Grafana HTTP API
```

This means the first Hermes capability depends on reading Grafana through its HTTP API.

Another example:

```text
Viewer Service Account Token -> Least Privilege
```

This means the read-only token is part of the least-privilege security model.

## Colors

Colors represent communities.

A community is a group of concepts that belong together.

In this graph, the main communities are:

```text
Grafana Read-Only Security
Hexagonal Core
Hermes Agent Vision
Public Private Boundary
Port Abstractions
```

When concepts share a color, they are part of the same area of understanding.

## Shaded Shapes

The shaded shapes are group relationships.

They mean: these concepts should be understood together.

### Hexagonal Layers

This group contains:

```text
Application Layer
Domain Layer
Hexagonal Architecture
HTTP Interface
Infrastructure Adapters
Ports
```

Read it as:

```text
These concepts together form the hexagonal architecture of Hermes.
```

### Security Boundary Model

This group contains:

```text
Viewer Service Account Token
Least Privilege
Read-Only Endpoints
Private Configuration
```

Read it as:

```text
These concepts together form the security boundary of Hermes.
```

This is important: Hermes is not safe because of one single decision. It is safer because several boundaries work together.

## Best Reading Order

Start from:

```text
Hermes Observability Agent
```

Then follow this path:

```text
Hermes Observability Agent
-> Bounded Observability Agent
-> Explicit Capabilities
-> grafana.read
```

After that, inspect the security path:

```text
grafana.read
-> Viewer Service Account Token
-> Least Privilege
-> Read-Only Endpoints
```

Finally, inspect the architecture path:

```text
Hermes Observability Agent
-> Hexagonal Architecture
-> Ports
-> GrafanaReader Port
```

## What This Graph Proves

The graph shows that Hermes is being designed around:

- explicit scope
- read-only access
- private configuration outside Git
- synthetic public demo data
- hexagonal architecture
- future extensibility

That is the central message of the project.
