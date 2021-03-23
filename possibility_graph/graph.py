from typing import FrozenSet, Dict
from possibility_graph.group import Group
from possibility_graph.rule import Rule, RuleType


class Graph:
    def __init__(self):
        self.groups = {}
        self.rules = {}
        self.rule_count = 0

    def add_group(self, group_name: str):
        if group_name not in self.groups:
            group = Group(group_name)
            self.groups[group_name] = group
            return group

    def add_groups(self, group_names_list):
        for name in group_names_list:
            self.add_group(name)

    def get_group(self, group_name: str) -> Group:
        return self.groups[group_name]

    @staticmethod
    def add_edge(node, other_node):
        node.add_edge(other_node)
        other_node.add_edge(node)

    @staticmethod
    def delete_edge(node, other_node):
        node.delete_edge(other_node)
        other_node.delete_edge(node)

    @staticmethod
    def get_triangle_nodes(node, other_node, third_group_name):
        neighbours = node.edges.get(third_group_name, set())
        other_neighbours = other_node.edges.get(third_group_name, set())
        return neighbours.intersection(other_neighbours)

    def cross_out_edge(self, node, other_node):
        self.delete_edge(node, other_node)
        removable_edges = self.find_removable_edges(node, other_node)
        self.cross_out_edges(removable_edges)

    def cross_out_edges(self, removable_edges_list):
        for edge in removable_edges_list:
            node, other_node = edge
            self.cross_out_edge(node, other_node)

    def find_removable_edges(self, node, other_node):
        group_name = node.group.name
        other_group_name = other_node.group.name
        removable_edges = []
        for rule_number in self.rules:
            rule = self.rules[rule_number]
            if group_name in rule.group_names and other_group_name in rule.group_names:
                own_edge = frozenset([group_name, other_group_name])
                own_rule_type = rule.edge_rules[own_edge]
                for edge in rule.edge_rules:
                    if edge == own_edge:
                        continue

                    for g_n in edge:
                        if group_name == g_n or other_group_name == g_n:
                            actual_group = g_n
                        else:
                            actual_pair_group = g_n

                    if actual_group == group_name:
                        actual_node = node
                        out_node = other_node
                    else:
                        actual_node = other_node
                        out_node = node

                    out_group = out_node.group.name

                    other_rule_type = rule.edge_rules[edge]

                    if other_rule_type == RuleType.Red and own_rule_type != RuleType.Pair:
                        pair_nodes = self.get_triangle_nodes(node, other_node, actual_pair_group)
                        for pair_node in pair_nodes:
                            removable_edges.append((actual_node, pair_node))

                    if other_rule_type == RuleType.Green:
                        pair_nodes = self.get_triangle_nodes(node, other_node, actual_pair_group)
                        for pair_node in pair_nodes:
                            out_nodes = self.get_triangle_nodes(actual_node, pair_node, out_group)
                            if len(out_nodes) == 0:
                                removable_edges.append((actual_node, pair_node))

        return removable_edges

    def add_rule(self, edge_rules: Dict[FrozenSet[str], 'RuleType'], node_rules: Dict[str, 'RuleType'] = None):
        self.rules[self.rule_count] = Rule(edge_rules, node_rules)
        self.rule_count += 1
