import pickle
import igraph as ig
import numpy as np
from collections import Counter

from centrality import random_walk_centrality


def inter_cluster(graph, subgraph1, subgraph2):
    """
    Compute the inter cluster as the Average Centroid Linkage Distance between two clusters.
    Returns the average centroid linkage distance between the two clusters.
    """
    # Compute central nodes for each cluster
    central_node1, _ = random_walk_centrality(subgraph1)
    central_node2, _ = random_walk_centrality(subgraph2)

    # Find the vertex indices of the central nodes in the original graph
    central_index1 = graph.vs.find(label=central_node1).index
    central_index2 = graph.vs.find(label=central_node2).index

    # Get vertex indices of nodes in each cluster
    cluster1_indices = [graph.vs.find(label=node["label"]).index for node in subgraph1.vs]
    cluster2_indices = [graph.vs.find(label=node["label"]).index for node in subgraph2.vs]

    # Calculate distances from central node of cluster1 to all nodes in cluster2
    distances1 = graph.distances(central_index1, cluster2_indices) 
    # Calculate distances from central node of cluster2 to all nodes in cluster1
    distances2 = graph.distances(central_index2, cluster1_indices) 

    # Calculate inter cluster
    avg_distance = (sum(distances1) + sum(distances2)) / (len(cluster1_indices) + len(cluster2_indices))

    return avg_distance

if __name__ == "__main__":
    # Load graph
    graph = ig.Graph.Read_Pickle("src\\files\\graph.pkl")

    # Load all saved subgraphs
    subgraphs = []
    i = 0
    while i != 2: # Test for only 2 subgraphs
        try:
            subgraphs.append(ig.Graph.Read_Pickle(f"src\\files\\subgraph{i}.pkl"))
            i += 1
        except FileNotFoundError:
            break
    print("Subgraphs loaded.")

    print(f"Inter cluster: {inter_cluster(graph, subgraphs[0], subgraphs[1]):.6f}")