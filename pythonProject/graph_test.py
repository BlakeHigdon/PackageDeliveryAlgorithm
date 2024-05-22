# Import the necessary modules
from graph import Graph
import csv

# Create an instance of Graph
graph = Graph()

# Initialize the graph with necessary data
graph.initialize_name_data()  # Initializes the names for the locations
graph.initialize_distance_data()  # Loads the distances between locations
graph.initialize_addresses()  # Builds the adjacency matrix with addresses and weights

# Call the print function to check the adjacency matrix
graph.print_adjacency_matrix()  # This should print the adjacency matrix to the terminal
