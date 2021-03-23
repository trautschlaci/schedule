from possibility_graph.node import Node


class Group:
    def __init__(self, name: str):
        self.name = name
        self.nodes = {}

    def add_node(self, node_name: str):
        if node_name not in self.nodes:
            node = Node(self, node_name)
            self.nodes[node_name] = node
            return node

    def add_nodes(self, nodes_names_list):
        for name in nodes_names_list:
            self.add_node(name)

    def get_node(self, node_name: str) -> Node:
        return self.nodes[node_name]

    def __repr__(self):
        return self.name
