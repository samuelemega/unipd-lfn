"""
  Author: Samuele Mega
"""

import igraph as ig
import pickle
import os

from leiden_compute_communities import compute_communities_modularity_vertex, compute_communities_significance_vertex

if __name__ == "__main__":
  graph = ig.Graph.Read_Pickle(os.path.join("files", "graph.pkl"))

  with open(os.path.join("files", "leiden_communities_modularity_vertex.pkl"), "wb") as file:
    pickle.dump(compute_communities_modularity_vertex(graph), file)

  print("[LOG] Generated: Leiden communities (Modularity Vertex)")

  with open(os.path.join("files", "leiden_communities_significance_vertex.pkl"), "wb") as file:
    pickle.dump(compute_communities_significance_vertex(graph), file)

  print("[LOG] Generated: Leiden communities (Significance Vertex)")
