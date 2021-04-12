from typing import FrozenSet, Dict, List
from possibility_graph.group import Group
from possibility_graph.rule import Rule, RuleType


class Graph:
    def __init__(self):
        self.groups: Dict[str, Group] = {}
        self.rules: List[Rule] = []
        self.infos: Dict[str, Dict[FrozenSet[str, str], ]] = {}

    def add_group(self, group_name: str, is_weak_group=False):
        if group_name in self.groups:
            return self.groups[group_name]

        group = Group(self, group_name, is_weak_group)
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
        node.group.delete_node(node.name)
        node.is_deleted = True

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
        self.delete_node(node)
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
                    edge_p_3 = frozenset([red_group, g])
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
                    do_delete_node = False
                    for neighbour in node.edges.get(pair_group, set()):
                        out_nodes = self.get_triangle_nodes(node, neighbour, out_group)
                        node_sets.append(out_nodes)
                        if len(out_nodes) == 0:
                            do_delete_node = True

                    if do_delete_node is False and rule.node_rules.get(out_group, None) == RuleType.Distinct:
                        do_delete_node = not self.is_separable(node_sets)

                    if do_delete_node:
                        removable_list.append(node)

        return removable_list

    def add_rule(self, edge_rules: Dict[FrozenSet[str], 'RuleType'], node_rules: Dict[str, 'RuleType'] = None):
        self.rules.append(Rule(edge_rules, node_rules))

    @staticmethod
    def edge_exists(node, other_node):
        if other_node.group.name not in node.edges:
            return False
        return other_node in node.edges[other_node.group.name]

    @staticmethod
    def node_exists(node):
        return node.name in node.group.nodes

    @staticmethod
    def is_separable(node_sets):
        all_nodes = set()
        for node_set in node_sets:
            all_nodes.update(node_set)
        return len(all_nodes) >= len(node_sets)

    def delete_group(self, group_name: str):
        group = self.get_group(group_name)
        while len(group.nodes) > 0:
            node = group.nodes.popitem()[1]
            for edge_set in node.edges.values():
                while len(edge_set) > 0:
                    edge_node = edge_set.pop()
                    edge_node.delete_edge(node, False)

        self.delete_rules_with_group(group_name)
        del self.groups[group_name]

    def merge_groups(self, main_group_name, sub_group_name):
        main_group = self.groups[main_group_name]
        for main_node in list(main_group.nodes.values()).copy():
            removable_list = []
            is_first = True
            main_new_name = main_node.name
            for sub_node in main_node.edges[sub_group_name]:
                if is_first:
                    main_new_name = f'{main_node.name} {sub_node.name}'
                    clone_node = main_node
                else:
                    clone_name = f'{main_node.name} {sub_node.name}'
                    clone_node = self.create_clone_node(main_node, clone_name)

                for clone_sub_node in clone_node.edges[sub_group_name]:
                    if clone_sub_node != sub_node:
                        removable_list.append((clone_node, clone_sub_node))

                is_first = False
            self.change_name(main_node, main_new_name)
            self.cross_out_edges_or_nodes(removable_list)

    def create_clone_node(self, node, clone_name):
        group = node.group
        clone_node = group.add_node(clone_name)
        for node_set in node.edges.values():
            for edge_node in node_set:
                self.add_edge(edge_node, clone_node)
        return clone_node

    @staticmethod
    def is_completely_separable(node_sets):
        all_nodes = {frozenset()}
        for i in range(len(node_sets)):
            temp_nodes = set()
            node_set = node_sets[i]
            for previous_node_set in all_nodes:
                for node in node_set:
                    temp_set = previous_node_set.union([node])
                    if len(temp_set) > i:
                        temp_nodes.add(temp_set)
            all_nodes = temp_nodes
        return len(all_nodes) > 0

    @staticmethod
    def change_name(node, new_node_name):
        node.group.nodes[new_node_name] = node.group.nodes.pop(node.name)
        node.name = new_node_name

    def delete_rules_with_group(self, group_name):
        self.rules = [rule for rule in self.rules if group_name not in rule.group_names]
