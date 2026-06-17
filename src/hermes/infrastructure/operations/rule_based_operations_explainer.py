from hermes.domain.metrics import OperationalSignal
from hermes.domain.operations import ExplanationConfidence, OperationalExplanation


class RuleBasedOperationsExplainer:
    """Public-safe deterministic explanations for synthetic operational signals."""

    def explain(self, signal: OperationalSignal) -> OperationalExplanation:
        if signal.name == "database":
            return OperationalExplanation(
                signal=signal.name,
                meaning="The database connectivity signal is reachable.",
                risk=(
                    "Low risk in the synthetic demo. In a real system this proves "
                    "connectivity, not query performance."
                ),
                possible_causes=(
                    "database connection is available",
                    "application can complete a basic database check",
                ),
                recommended_checks=(
                    "check latency separately",
                    "check query errors separately",
                    "verify connection pool health in private monitoring",
                ),
                safe_actions=(
                    "keep the signal as a baseline health check",
                    "document what this signal proves and what it does not prove",
                ),
                unsafe_actions=(
                    "assume every database query is fast",
                    "change database configuration from Hermes",
                ),
                confidence=ExplanationConfidence.HIGH,
            )

        if signal.name == "api_latency":
            return OperationalExplanation(
                signal=signal.name,
                meaning="API latency is stable in the public demo.",
                risk=(
                    "Low risk while stable. Real systems should compare p50, p95, "
                    "and p99 latency before concluding users are unaffected."
                ),
                possible_causes=(
                    "traffic is stable",
                    "application response times are not changing significantly",
                ),
                recommended_checks=(
                    "compare latency percentiles",
                    "separate slow endpoints from global averages",
                    "check whether recent deployments changed response times",
                ),
                safe_actions=(
                    "keep latency dashboards visible",
                    "define warning thresholds for p95 and p99 latency",
                ),
                unsafe_actions=(
                    "assume all endpoints are fast from one stable signal",
                    "ignore user-facing latency because the average looks stable",
                ),
                confidence=ExplanationConfidence.HIGH,
            )

        if signal.name == "worker_queue":
            return OperationalExplanation(
                signal=signal.name,
                meaning="Jobs are waiting longer before being processed.",
                risk=(
                    "If the queue keeps growing, users may experience delayed "
                    "background work."
                ),
                possible_causes=(
                    "workers are slower than incoming jobs",
                    "one worker group is stopped",
                    "a recent job type is taking longer than expected",
                    "jobs are failing and retrying",
                ),
                recommended_checks=(
                    "check worker health",
                    "compare queue trend over the last few minutes",
                    "look for repeated job failures",
                    "check whether a deployment happened recently",
                ),
                safe_actions=(
                    "document the observation",
                    "inspect worker logs through the approved application boundary",
                    "review whether worker capacity is enough",
                ),
                unsafe_actions=(
                    "delete queued messages without analysis",
                    "restart production automatically",
                    "change infrastructure from Hermes without approval",
                ),
                confidence=ExplanationConfidence.HIGH,
            )

        if signal.name == "scrape_targets":
            return OperationalExplanation(
                signal=signal.name,
                meaning="The monitoring collector can reach the synthetic targets.",
                risk=(
                    "Low risk while stable. A reachable scrape target means metrics "
                    "can be collected, not that the business feature is healthy."
                ),
                possible_causes=(
                    "monitoring target is reachable",
                    "metrics endpoint is responding",
                ),
                recommended_checks=(
                    "check application-specific health separately",
                    "check missing metrics or dashboard gaps",
                    "verify alerts cover important service behavior",
                ),
                safe_actions=(
                    "keep scrape target health visible",
                    "document which service behavior each target represents",
                ),
                unsafe_actions=(
                    "assume the service is fully healthy from scrape success alone",
                    "ignore missing business metrics",
                ),
                confidence=ExplanationConfidence.HIGH,
            )

        return OperationalExplanation(
            signal=signal.name,
            meaning=f"Hermes has a bounded signal named {signal.name}.",
            risk="Risk cannot be determined confidently from this generic explanation.",
            possible_causes=("signal-specific causes are not defined yet",),
            recommended_checks=(
                "review the signal source",
                "document what this signal proves",
                "add a specific explanation rule if this signal is important",
            ),
            safe_actions=("treat this as an unknown signal until documented",),
            unsafe_actions=(
                "claim a root cause without evidence",
                "execute operational actions from a generic explanation",
            ),
            confidence=ExplanationConfidence.LOW,
        )
