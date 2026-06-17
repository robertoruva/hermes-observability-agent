# LLM Private Layer Decision

This note records an architecture decision:

```text
The public Hermes repository must not require an LLM.
LLM usage belongs to a future private optional layer.
```

## Context

Hermes can already demonstrate useful behavior without an LLM:

```text
metrics.read
-> operations.explain
-> maintenance.plan.generate
-> actions.propose
```

The public implementation is deterministic and rule-based.

That is intentional.

It means a visitor can run Hermes without:

- provider accounts
- API keys
- token costs
- prompt configuration
- private infrastructure access

## Decision

The public repository stays deterministic.

The LLM layer is reserved for private deployments.

Public Hermes:

```text
deterministic
synthetic data
no LLM key required
safe demo
no secrets
no execution
```

Private Hermes may add:

```text
optional LLM provider
private application API context
richer explanations
better prioritization
draft reports
reviewable recommendations
human approval flow
audit logging
```

## Why This Is Safer

An LLM can improve interpretation, but it should not become the security boundary.

Hermes's safety comes from:

- explicit capabilities
- ports and adapters
- synthetic public data
- private configuration outside Git
- no mutation endpoints
- approval requirements
- application API boundary
- Docker-first reproducibility

The LLM can sit on top of those boundaries later.

It should not replace them.

## Public Repository Rule

The public repository must not require:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`
- provider-specific credentials
- private prompt files
- private model configuration

If an example mentions LLM usage, it must say:

```text
Private optional layer, not required for the public demo.
```

## Future Private Shape

A private deployment could look like:

```text
Hermes public core
-> private application API adapter
-> filtered operational context
-> optional LLM explainer or proposer
-> human review
-> approved action outside Hermes
```

The LLM would help draft better explanations or proposals.

It still would not execute infrastructure changes.

## What The LLM May Do Privately

In a private deployment, an LLM may help with:

- richer operational summaries
- clearer incident explanations
- maintenance plan wording
- action proposal wording
- report drafts
- interview-style or learning explanations
- comparing several safe signals together

## What The LLM Must Not Do

The LLM must not:

- receive raw secrets
- receive unrestricted logs
- receive customer data unnecessarily
- execute commands
- call mutation endpoints
- bypass approval
- invent root causes as facts
- hide uncertainty

## Deterministic Fallback

Every important public behavior should have a deterministic fallback.

That means Hermes remains useful when:

- no LLM key exists
- the provider is unavailable
- a private deployment disables LLM features
- deterministic tests need stable output

## Professional Rationale

This decision is useful to explain professionally:

```text
I separated deterministic public behavior from optional private LLM behavior.
The public project is easy to run and safe to inspect, while private deployments
can add LLM intelligence only after authentication, filtering, approval, and
audit boundaries are defined.
```

That shows maturity because the LLM is treated as a capability amplifier, not as a security model.
