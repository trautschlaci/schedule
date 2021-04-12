import enum
from typing import FrozenSet, Dict


class Rule:
    def __init__(self, edge_rules: Dict[FrozenSet[str], 'RuleType'], node_rules: Dict[str, 'RuleType'] = None):
        self.edge_rules = edge_rules
        self.node_rules = node_rules
        self.group_names = set()

        for edge_rule in edge_rules:
            self.group_names.update(edge_rule)
        if len(self.group_names) > 3:
            print("Invalid rule")

        if self.node_rules is None:
            self.node_rules = {}

    def __repr__(self):
        return self.group_names.__repr__()


class RuleType(enum.Enum):
    Normal = 1
    Green = 2
    Red = 3
    Pair = 4
    Distinct = 5
