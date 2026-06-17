from hermes.infrastructure.maintenance.rule_based_maintenance_planner import (
    RuleBasedMaintenancePlanner,
)
from hermes.ports.maintenance_planner import MaintenancePlanner


def create_maintenance_planner() -> MaintenancePlanner:
    return RuleBasedMaintenancePlanner()
