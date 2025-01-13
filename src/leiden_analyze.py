"""
  Author: Samuele Mega
"""

import pickle
import json
import igraph as ig
import os

from helpers import weighted_soergel
from leiden_helpers import communities_info

"""
  main
"""
if __name__ == "__main__":

  graph = ig.Graph.Read_Pickle("files/graph.pkl")

  with open(os.path.join("files", "leiden_communities_modularity_vertex.pkl"), "br") as file:
    communities_modularity_vertex = pickle.load(file)

  with open(os.path.join("files", "leiden_communities_significance_vertex.pkl"), "br") as file:
    communities_significance_vertex = pickle.load(file)

  with open(os.path.joion("files", "analysis_leiden_communities_modularity_vertex.json"), "w", encoding="utf-8") as file:
    json.dump(communities_info(graph, communities_modularity_vertex, 10), file, indent=2, ensure_ascii=False)

  with open(os.path.joion("files", "communities_significance_vertex.json"), "w", encoding="utf-8") as file:
    json.dump(communities_info(graph, communities_significance_vertex, 10), file, indent=2, ensure_ascii=False)
