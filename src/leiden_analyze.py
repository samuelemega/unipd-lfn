"""
  Author: Samuele Mega
"""

import pickle
import json
import igraph as ig

from helpers import weighted_soergel
from leiden_helpers import communities_info

"""
  get_community_categories
"""
def get_community_categories(graph, community):
  categories = []

  for item in community:
    categories += graph.vs[item]["categories"]

  return categories

"""
  main
"""
if __name__ == "__main__":

  graph = ig.Graph.Read_Pickle("files/graph.pkl")

  with open("files/leiden_communities_modularity_vertex.pkl", "br") as file:
    communities_modularity_vertex = pickle.load(file)

  with open("files/leiden_communities_significance_vertex.pkl", "br") as file:
    communities_significance_vertex = pickle.load(file)

  with open("files/analysis_leiden_communities_modularity_vertex.json", "w", encoding="utf-8") as file:
    json.dump(communities_info(graph, communities_modularity_vertex, 10), file, indent=2, ensure_ascii=False)

  with open("files/analysis_leiden_communities_significance_vertex.json", "w", encoding="utf-8") as file:
    json.dump(communities_info(graph, communities_significance_vertex, 10), file, indent=2, ensure_ascii=False)
