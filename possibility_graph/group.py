from possibility_graph.node import Node


class Group:
    def __init__(self, graph, name: str, is_weak_group=False):
        self.graph = graph
        self.name = name
        self.nodes = {}
        self.is_weak_group = is_weak_group

    def add_node(self, node_name: str):
        if node_name in self.nodes:
            return self.nodes[node_name]

        node = Node(self, node_name)
        self.nodes[node_name] = node
        return node

    def add_nodes(self, nodes_names_list):
        for name in nodes_names_list:
            self.add_node(name)

    def get_node(self, node_name: str) -> Node:
        return self.nodes[node_name]

    def delete_node(self, node_name: str):
        del self.nodes[node_name]

    def add_edge_to_all_nodes(self, other_node):
        for node in self.nodes.values():
            self.graph.add_edge(node, other_node)

    def __repr__(self):
        return self.name
