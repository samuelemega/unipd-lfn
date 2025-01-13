"""
  Author: Samuele Mega
"""

import pickle
import igraph as ig
import leidenalg as la
import os

if __name__ == "__main__":
  graph = ig.Graph.Read_Pickle(os.path.open("files", "graph.pkl"))

  with open("files/communities.pkl", "wb") as file:
    pickle.dump(communities, file)
