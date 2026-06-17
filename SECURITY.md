# Security Policy

Hermes Observability Agent is designed around least privilege and public-safe examples.

## Supported Versions

Hermes is currently pre-release. Security updates apply to the latest version of the main branch.

## Reporting A Vulnerability

Please do not open a public issue containing secrets, tokens, private URLs, logs, or sensitive infrastructure details.

If you find a security issue, report it privately to the maintainer.

Until a dedicated security contact is configured, use the repository owner's preferred private contact channel.

## Sensitive Data Policy

The public repository must not contain:

- real tokens or API keys
- private Grafana URLs
- internal IP addresses
- customer data
- production logs
- private dashboard exports
- screenshots from private systems

## Intended Security Model

Hermes should limit risk through:

- read-only credentials
- explicit capabilities
- synthetic public demo data
- ignored private configuration files
- narrow HTTP endpoints
- hexagonal separation between core logic and infrastructure adapters

Read-only access still requires care. Observability data can reveal infrastructure structure, traffic patterns, incidents, and business information.
