from hermes.infrastructure.actions.rule_based_action_proposer import (
    RuleBasedActionProposer,
)
from hermes.ports.action_proposer import ActionProposer


def create_action_proposer() -> ActionProposer:
    return RuleBasedActionProposer()
