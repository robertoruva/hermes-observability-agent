# Graph Report - .  (2026-06-23)

## Corpus Check
- Deterministic local refresh generated from README, knowledge notes, and implementation surface.
- No LLM API key was used, so this graph favors explicit project structure over deep semantic inference.
- Updated to include the first manual demo guides: `knowledge/38-first-manual-demo.md` and `knowledge/39-first-plan-and-proposal-demo.md`.

## Summary
- 55 nodes · 93 edges · 8 communities
- Extraction: 93 EXTRACTED · 0 INFERRED · 0 AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Public_Safety_Model|Public Safety Model]] (7 nodes)
- [[_COMMUNITY_Hexagonal_Architecture|Hexagonal Architecture]] (6 nodes)
- [[_COMMUNITY_Capability_Pipeline|Capability Pipeline]] (8 nodes)
- [[_COMMUNITY_Docker_Runtime|Docker Runtime]] (6 nodes)
- [[_COMMUNITY_Public_Demo_Hardening|Public Demo Hardening]] (8 nodes)
- [[_COMMUNITY_Implementation_Surface|Implementation Surface]] (10 nodes)
- [[_COMMUNITY_Knowledge_Guides|Knowledge Guides]] (5 nodes)
- [[_COMMUNITY_Release_Readiness|Release Readiness]] (5 nodes)

## God Nodes (most connected - your core abstractions)
1. `actions.propose` - 11 edges
2. `Hermes Observability Agent` - 8 edges
3. `Public Demo Hardening` - 8 edges
4. `operations.explain` - 8 edges
5. `Endpoint Demo Flow` - 8 edges
6. `FastAPI App` - 7 edges
7. `metrics.read` - 7 edges
8. `maintenance.plan.generate` - 7 edges
9. `Public Release Checklist` - 7 edges
10. `LLM Private Layer Decision` - 7 edges

## Key Updated Connections
- `First Manual Demo` --> `operations.explain`
- `First Manual Demo` --> `Endpoint Demo Flow`
- `First Manual Demo` --> `First Plan And Proposal Demo`
- `First Plan And Proposal Demo` --> `maintenance.plan.generate`
- `First Plan And Proposal Demo` --> `actions.propose`
- `First Plan And Proposal Demo` --> `Wait For Approval`

## Hyperedges (group relationships)
- **Capability Pipeline** — grafana.read, metrics.read, operations.explain, maintenance.plan.generate, actions.propose, Wait For Approval [EXTRACTED 1.00]
- **Hexagonal Layers** — Domain Layer, Application Layer, Ports, Infrastructure Adapters, HTTP Interface [EXTRACTED 1.00]
- **Public Safety Model** — Public Repository, Private Configuration, Synthetic Demo Data, Least Privilege, No Execution Boundary [EXTRACTED 1.00]
- **Demo Story** — How To Demo Hermes, Endpoint Demo Flow, actions.propose, No Execution Boundary [EXTRACTED 1.00]
- **Release Readiness Model** — Public Release Checklist, LLM Private Layer Decision, Deterministic Public Behavior, Private Optional LLM, Release Gate [EXTRACTED 1.00]
- **First Manual Demo Story** — First Manual Demo, First Plan And Proposal Demo, operations.explain, maintenance.plan.generate, actions.propose, Wait For Approval [EXTRACTED 1.00]

## Communities (8 total)

### Community 0 - "Public Safety Model"
Nodes (7): Bounded Observability Agent, Public Repository, Private Configuration, Synthetic Demo Data, Least Privilege, No Execution Boundary, Application API Boundary

### Community 1 - "Hexagonal Architecture"
Nodes (6): Hexagonal Architecture, Domain Layer, Application Layer, Ports, Infrastructure Adapters, HTTP Interface

### Community 2 - "Capability Pipeline"
Nodes (8): grafana.read, metrics.read, operations.explain, maintenance.plan.generate, actions.propose, Wait For Approval, Roadmap And Learning Path, Capability Matrix

### Community 3 - "Docker Runtime"
Nodes (6): Docker First Workflow, Dockerfile, Demo Compose File, Test Compose File, Container Runtime Guard, Docker Tests

### Community 4 - "Public Demo Hardening"
Nodes (8): Hermes Observability Agent, Public Demo Hardening, How To Demo Hermes, Endpoint Demo Flow, Public Checklist, Knowledge Graph Refresh, First Manual Demo, First Plan And Proposal Demo

### Community 5 - "Implementation Surface"
Nodes (10): GrafanaReader Port, MetricsReader Port, OperationsExplainer Port, MaintenancePlanner Port, ActionProposer Port, FakeMetricsReader, RuleBasedOperationsExplainer, RuleBasedMaintenancePlanner, RuleBasedActionProposer, FastAPI App

### Community 6 - "Knowledge Guides"
Nodes (5): Signals Reading Guide, Explanations Reading Guide, Action Proposals Reading Guide, Why These Files Exist, Graph Reading Guide

### Community 7 - "Release Readiness"
Nodes (5): Public Release Checklist, LLM Private Layer Decision, Deterministic Public Behavior, Private Optional LLM, Release Gate

## Suggested Questions

- How does the first manual demo prove the explain -> plan -> propose flow?
- Why does Hermes keep action proposals separate from execution?
- Which endpoints should a new user run first in the public demo?
- How does the manual demo support the public-to-private transition?
