"""
  Author: Samuele Mega
"""

import pickle
import igraph as ig

if __name__ == "__main__":

  with open("files/nodes.pkl", "br") as file:
    nodes = pickle.load(file)

  # Computing the labels of the vertices and edges

  labels_indeces = { label: index for index, label in enumerate(list(nodes.keys())) }
  edges = []

  for label, node in nodes.items():

    parent_index = labels_indeces[label]

    for link in node["links"]:
      if link is not None:
        edges.append((parent_index, labels_indeces[link]))

  # Creating the graph

  graph = ig.Graph(n=len(labels_indeces), directed=True)
  graph.add_edges(edges)

  for label, node in nodes.items():
    graph.vs[labels_indeces[label]]["label"] = label
    graph.vs[labels_indeces[label]]["categories"] = node["categories"]

  # Finding and saving the largest component of the graph

  largest_component = max(graph.connected_components(), key=len)

  subgraph = graph.subgraph(largest_component)

  subgraph.write_pickle("files/graph.pkl")
