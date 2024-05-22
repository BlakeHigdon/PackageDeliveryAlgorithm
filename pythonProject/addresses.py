from edges import Edge


class Addresses:
    def __init__(self, name, edges):
        self.name = name
        self.edges = edges

    # returns name of address and edges
    # time complexity O(n)
    def __str__(self):
        return f"Name: {self.name}, Edges: {self.edges}"

    # add an edge to an address
    # time complexity O(n)
    def add(self, target, weight):
        self.edges.add(target, Edge(start_node=self.name, end_node=target, weight=weight))
