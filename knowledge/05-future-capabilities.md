# Future Capabilities

Hermes should be designed to grow without becoming tightly coupled.

Each new capability should follow the same pattern:

```text
capability -> port -> use case -> adapter
```

The current capability matrix is documented in `knowledge/22-capability-matrix.md`.

## Possible Capabilities

```text
logs.read
alerts.read
alpha.status.read
reports.generate
incidents.summarize
```

## Rule For Growth

Before adding a capability, answer:

- What can Hermes do?
- What can Hermes not do?
- What credential is required?
- What data could be exposed?
- Is this safe for the public demo?
- What belongs in private configuration?

This keeps Hermes understandable as it grows.
