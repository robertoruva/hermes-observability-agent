# Contributing

Thanks for considering a contribution to Hermes Observability Agent.

Hermes is designed as a small, bounded observability agent. Contributions should preserve that spirit: explicit scope, least privilege, safe defaults, and clear architecture.

## Project Principles

- Keep capabilities explicit.
- Prefer read-only integrations by default.
- Keep private configuration out of Git.
- Preserve hexagonal architecture boundaries.
- Use synthetic data for public examples and demos.
- Avoid turning Hermes into an unrestricted proxy.

## Good First Contributions

- Improve knowledge notes.
- Clarify README sections.
- Add tests around existing behavior.
- Improve demo data.
- Add safer configuration examples.
- Improve error messages.

## Before Opening A Pull Request

Please check that:

- no real secrets are committed
- `.env` is not committed
- examples use fake or synthetic data
- changes are documented in the knowledge tree when they affect architecture
- tests pass when implementation exists

## Architecture Notes

Hermes follows a hexagonal architecture approach:

```text
interfaces -> application -> ports/domain
infrastructure -> ports/domain
```

Application code should depend on ports and domain concepts, not directly on external APIs such as Grafana.

## Security Reminder

Do not include:

- real Grafana URLs
- service account tokens
- internal IP addresses
- private dashboard exports
- logs from private systems
- customer or production data

If you are unsure whether something is safe to publish, treat it as private.
