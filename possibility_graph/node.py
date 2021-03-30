class Node:
    def __init__(self, group, name: str):
        self.group = group
        self.name = name
        self.edges = {}
        self.is_deleted = False

    def add_edge(self, other_node):
        other_group_name = other_node.group.name
        if other_group_name not in self.edges:
            self.edges[other_group_name] = set()

        self.edges[other_group_name].add(other_node)

    def delete_edge(self, other_node, safe_delete=True):
        group_name = other_node.group.name
        self.edges[group_name].remove(other_node)

        if len(self.edges[group_name]) == 0:
            if not self.is_deleted and safe_delete:
                if self.group.is_weak_group:
                    self.group.graph.cross_out_node(self)
                else:
                    print(f"All {group_name} deleted from {self.name}")
            else:
                del self.edges[group_name]

    def __repr__(self):
        return self.name

