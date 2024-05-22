import csv
from hashmap import HashMap
from edges import Edge
from addresses import Addresses


# overall class time complexity is O(N^2)
class Graph:
    def __init__(self):
        self.locations = [None] * 27
        self.distances = []
        self.adjacency_matrix = HashMap()

    def initialize_name_data(self):
        with open("WGUPS Distance Table(1).csv") as csvfile:
            reader = csv.reader(csvfile)
            distances_names = list(reader)
            i = 0
        for entry in distances_names:
            self.locations[i] = entry
            i += 1

    def initialize_distance_data(self):
        with open("distances.csv") as csvfile:
            reader = csv.reader(csvfile)
            self.distances = list(reader)

    def initialize_addresses(self):
        for i in range(len(self.distances)):
            for j in range(len(self.distances)):
                if j < i:
                    self.add_address(start_node=self.locations[i][1],
                                     end_node=self.locations[j][1],
                                     weight=self.distances[i][j])
                    # print(f"Added edge: {start_node} -> {end_node} with weight {self.distances[i][j]}")
                if j > i:
                    self.add_address(start_node=self.locations[i][1],
                                     end_node=self.locations[j][1],
                                     weight=self.distances[j][i])
                    # print(f"Added edge: {start_node} -> {end_node} with weight {self.distances[j][i]}")

    def add_address(self, start_node, end_node, weight):
        node = self.adjacency_matrix.get(start_node)
        if node is not None:
            node.edges.append(Edge(start_node, end_node, weight))
            self.adjacency_matrix.add(start_node, node)
        else:
            self.adjacency_matrix.add(start_node, Addresses(start_node, [Edge(start_node, end_node, weight)]))

    def print_adjacency_matrix(self):
        print("Adjacency Matrix:")
        for key in self.adjacency_matrix.keys():
            node = self.adjacency_matrix.get(key)
            print(f"Node: {key}")
            if node:
                for edge in node.edges:
                    print(f" - {edge.start_node} -> {edge.end_node} with weight {edge.weight}")




