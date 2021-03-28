from typing import FrozenSet, Dict, List
from possibility_graph.group import Group
from possibility_graph.rule import Rule, RuleType


class Graph:
    def __init__(self):
        self.groups: Dict[str, Group] = {}
        self.rules: List[Rule] = []
        self.infos: Dict[str, Dict[FrozenSet[str, str], ]] = {}

    def add_group(self, group_name: str):
        if group_name in self.groups:
            return self.groups[group_name]

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
    def delete_node(node):
        node.group.delete_node(node)

    @staticmethod
    def get_triangle_nodes(node, other_node, third_group_name):
        neighbours = node.edges.get(third_group_name, set())
        other_neighbours = other_node.edges.get(third_group_name, set())
        return neighbours.intersection(other_neighbours)

    def cross_out_edge(self, node, other_node):
        if not self.edge_exists(node, other_node):
            return
        self.delete_edge(node, other_node)
        removable_list = self.find_removable_edges_or_nodes(node, other_node)
        self.cross_out_edges_or_nodes(removable_list)

    def cross_out_node(self, node):
        if not self.node_exists(node):
            return
        removable_list = []
        for node_set in node.edges.values():
            for other_node in node_set:
                removable_list.append((node, other_node))
        self.cross_out_edges_or_nodes(removable_list)

    def cross_out_edges_or_nodes(self, removable_list):
        for entity in removable_list:
            if type(entity) == tuple:
                node, other_node = entity
                self.cross_out_edge(node, other_node)
            else:
                self.cross_out_node(entity)

    def find_removable_edges_or_nodes(self, node1, node2):
        group1 = node1.group.name
        group2 = node2.group.name
        removable_list = []
        for rule in self.rules:
            if group1 not in rule.group_names or group2 not in rule.group_names:
                continue

            group3 = rule.group_names.difference({group1, group2}).pop()
            own_edge = frozenset([group1, group2])
            own_rule_type = rule.edge_rules[own_edge]

            for rule_edge in rule.edge_rules:
                if rule_edge == own_edge:
                    continue

                if group1 in rule_edge:
                    common_node = node1
                    out_node = node2
                else:
                    common_node = node2
                    out_node = node1

                out_group = out_node.group.name

                edge_rule_type = rule.edge_rules[rule_edge]

                if edge_rule_type == RuleType.Red and own_rule_type != RuleType.Pair:
                    triangle_nodes = self.get_triangle_nodes(node1, node2, group3)
                    for node3 in triangle_nodes:
                        removable_list.append((common_node, node3))

                if edge_rule_type == RuleType.Green:
                    triangle_nodes = self.get_triangle_nodes(node1, node2, group3)
                    for node3 in triangle_nodes:
                        out_nodes = self.get_triangle_nodes(common_node, node3, out_group)
                        if len(out_nodes) == 0:
                            removable_list.append((common_node, node3))

            if own_rule_type == RuleType.Pair:
                continue

            for red_group in rule.node_rules:
                if rule.node_rules[red_group] != RuleType.Red:
                    continue

                pair_group = ""
                for g in rule.group_names.difference({red_group}):
                    edge_p_3 = frozenset([red_group, pair_group])
                    if rule.edge_rules[edge_p_3] == RuleType.Pair:
                        pair_group = g
                        break

                out_group = rule.group_names.difference({red_group, pair_group}).pop()

                if group1 == red_group:
                    red_nodes = {node1}
                elif group2 == red_group:
                    red_nodes = {node2}
                else:
                    red_nodes = self.get_triangle_nodes(node1, node2, group3)

                for node in red_nodes:
                    node_sets = []
                    delete_node = False
                    for neighbour in node.edges.get(pair_group, set()):
                        out_nodes = self.get_triangle_nodes(node, neighbour, out_group)
                        node_sets.append(out_nodes)
                        if len(out_nodes) == 0:
                            delete_node = True

                    if delete_node is False and rule.node_rules.get(out_group, None) == RuleType.Distinct:
                        delete_node = not self.is_separable(node_sets)

                    if delete_node:
                        removable_list.append(node)

        return removable_list

    def add_rule(self, edge_rules: Dict[FrozenSet[str], 'RuleType'], node_rules: Dict[str, 'RuleType'] = None):
        self.rules.append(Rule(edge_rules, node_rules))

    @staticmethod
    def edge_exists(node, other_node):
        return other_node in node.edges[other_node.group.name]

    @staticmethod
    def node_exists(node):
        return node.name in node.group.nodes

    @staticmethod
    def is_separable(node_sets):
        # TODO: Improve algorithm
        all_nodes = set()
        for node_set in node_sets:
            all_nodes.update(node_set)
        return len(all_nodes) >= len(node_sets)
