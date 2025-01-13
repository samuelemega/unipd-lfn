"""
  Author: Samuele Mega
"""

import pickle
import igraph as ig
import leidenalg as la

if __name__ == "__main__":
  graph = ig.Graph.Read_Pickle("files/graph.pkl")

  with open("files/communities.pkl", "wb") as file:
    pickle.dump(communities, file)
