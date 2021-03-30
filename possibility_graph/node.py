class Node:
    def __init__(self, group, name: str):
        self.group = group
        self.name = name
        self.edges = {}

    def add_edge(self, other_node):
        other_group_name = other_node.group.name
        if other_group_name not in self.edges:
            self.edges[other_group_name] = set()

        self.edges[other_group_name].add(other_node)

    def delete_edge(self, other_node, safe_delete=True):
        group_name = other_node.group.name
        self.edges[group_name].remove(other_node)

        if len(self.edges[group_name]) == 0:
            if safe_delete:
                print(f"All {group_name} deleted from {self.name}")
            else:
                del self.edges[group_name]

    def __repr__(self):
        return self.name

