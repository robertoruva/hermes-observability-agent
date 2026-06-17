# Graph Report - .  (2026-06-17)

## Corpus Check
- Deterministic local refresh generated from README, knowledge notes, and implementation surface.
- No LLM API key was used, so this graph favors explicit project structure over deep semantic inference.

## Summary
- 53 nodes · 85 edges · 8 communities
- Extraction: 85 EXTRACTED · 0 INFERRED · 0 AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Public_Safety_Model|Public Safety Model]] (7 nodes)
- [[_COMMUNITY_Hexagonal_Architecture|Hexagonal Architecture]] (6 nodes)
- [[_COMMUNITY_Capability_Pipeline|Capability Pipeline]] (8 nodes)
- [[_COMMUNITY_Docker_Runtime|Docker Runtime]] (6 nodes)
- [[_COMMUNITY_Public_Demo_Hardening|Public Demo Hardening]] (6 nodes)
- [[_COMMUNITY_Implementation_Surface|Implementation Surface]] (10 nodes)
- [[_COMMUNITY_Knowledge_Guides|Knowledge Guides]] (5 nodes)
- [[_COMMUNITY_Release_Readiness|Release Readiness]] (5 nodes)

## God Nodes (most connected - your core abstractions)
1. `actions.propose` - 10 edges
2. `Hermes Observability Agent` - 8 edges
3. `Public Demo Hardening` - 8 edges
4. `metrics.read` - 7 edges
5. `operations.explain` - 7 edges
6. `FastAPI App` - 7 edges
7. `Public Release Checklist` - 7 edges
8. `LLM Private Layer Decision` - 7 edges
9. `Hexagonal Architecture` - 6 edges
10. `Ports` - 6 edges

## Key Updated Connections
- `Public Release Checklist` --> `Release Gate`
- `LLM Private Layer Decision` --> `Deterministic Public Behavior`
- `LLM Private Layer Decision` --> `Private Optional LLM`
- `Public Release Checklist` --> `No Execution Boundary`
- `Private Optional LLM` --> `Application API Boundary`

## Hyperedges (group relationships)
- **Capability Pipeline** — grafana.read, metrics.read, operations.explain, maintenance.plan.generate, actions.propose, Wait For Approval [EXTRACTED 1.00]
- **Hexagonal Layers** — Domain Layer, Application Layer, Ports, Infrastructure Adapters, HTTP Interface [EXTRACTED 1.00]
- **Public Safety Model** — Public Repository, Private Configuration, Synthetic Demo Data, Least Privilege, No Execution Boundary [EXTRACTED 1.00]
- **Demo Story** — How To Demo Hermes, Endpoint Demo Flow, actions.propose, No Execution Boundary [EXTRACTED 1.00]
- **Release Readiness Model** — Public Release Checklist, LLM Private Layer Decision, Deterministic Public Behavior, Private Optional LLM, Release Gate [EXTRACTED 1.00]

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
Nodes (6): Hermes Observability Agent, Public Demo Hardening, How To Demo Hermes, Endpoint Demo Flow, Public Checklist, Knowledge Graph Refresh

### Community 5 - "Implementation Surface"
Nodes (10): GrafanaReader Port, MetricsReader Port, OperationsExplainer Port, MaintenancePlanner Port, ActionProposer Port, FakeMetricsReader, RuleBasedOperationsExplainer, RuleBasedMaintenancePlanner, RuleBasedActionProposer, FastAPI App

### Community 6 - "Knowledge Guides"
Nodes (5): Signals Reading Guide, Explanations Reading Guide, Action Proposals Reading Guide, Why These Files Exist, Graph Reading Guide

### Community 7 - "Release Readiness"
Nodes (5): Public Release Checklist, LLM Private Layer Decision, Deterministic Public Behavior, Private Optional LLM, Release Gate

## Suggested Questions

- Why does Hermes keep deterministic public behavior separate from private optional LLM behavior?
- What must be true before publishing Hermes publicly?
- How does the release checklist enforce the no-execution boundary?
- Which private capabilities could use an LLM without making it the security boundary?
