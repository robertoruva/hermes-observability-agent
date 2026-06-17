# HTTP Interface Decision

Hermes currently uses FastAPI as its first HTTP interface.

This is an implementation decision for the first adapter, not a permanent identity for the project.

## Decision

Use FastAPI for the first Hermes HTTP API.

## Why FastAPI

Hermes needs a small read-only HTTP surface:

```text
GET /health
GET /api/grafana/search
GET /api/grafana/dashboards/{uid}
```

FastAPI is a good fit because it is:

- simple for small APIs
- fast to understand
- easy to Dockerize
- good for JSON APIs
- able to generate interactive API documentation automatically
- lightweight enough for a bounded agent

The automatic API documentation is useful for an open source project because people can inspect and test endpoints quickly.

## Why Not Django First

Django is a strong framework, but it is larger than Hermes needs for the first version.

Django is usually a better fit when the project needs:

- a database-backed web application
- user management
- an admin panel
- templates and server-rendered pages
- complex business workflows
- a larger monolithic application

Hermes v0.1 does not need those things yet.

Hermes needs a small API around explicit read-only capabilities.

## Hexagonal Boundary

FastAPI lives in:

```text
src/hermes/interfaces/http/
```

It should not leak into:

```text
src/hermes/domain/
src/hermes/application/
src/hermes/ports/
```

This means Hermes can replace FastAPI later without rewriting the core.

## Future Agents

If Hermes later controls documentation, the first question should not be:

```text
Should this be Django or FastAPI?
```

The first question should be:

```text
Is this a new capability inside Hermes, or a separate service?
```

## Add As A Hermes Capability

Add it inside Hermes when it shares the same purpose and security model.

Example:

```text
documentation.read
documentation.search
documentation.summarize
```

This would follow the same pattern:

```text
capability -> use case -> port -> adapter
```

FastAPI could expose it through HTTP, but the capability itself would not depend on FastAPI.

## Create A Separate Service

Create a separate service when the documentation agent has a different lifecycle, different permissions, different storage needs, or a different audience.

For example, a documentation system may eventually need:

- database models
- user roles
- editing workflows
- approvals
- version history
- an admin interface

At that point, Django could be a stronger choice.

## Rule Of Thumb

Use FastAPI when Hermes needs a small API around bounded capabilities.

Use Django when the project becomes a full web application with persistence, users, admin workflows, and rich product behavior.

The architecture should make either option possible.
