"""
  Author: Marco Facco
"""

import pickle
import igraph as ig
import os

if __name__ == "__main__":
  g = ig.Graph.Read_Pickle(os.path.join("files", "graph.pkl"))
  ug = g.as_undirected()

  # Detect communities using the Label Propagation algorithm
  com = ug.community_label_propagation()
  num_nodes = ug.vcount()
  subcoms = com.subgraphs()
  i = 0

  for sub in subcoms:
    with open(os.path.join("files", f"labelpropagation_subgraph_{repr(i)}.pkl"), "wb") as file:
      sRatio = sub.vcount() / num_nodes
      pickle.dump(sub, file)
      i += 1
