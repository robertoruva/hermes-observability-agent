from hermes.infrastructure.operations.rule_based_operations_explainer import (
    RuleBasedOperationsExplainer,
)
from hermes.ports.operations_explainer import OperationsExplainer


def create_operations_explainer() -> OperationsExplainer:
    return RuleBasedOperationsExplainer()
