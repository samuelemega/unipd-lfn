"""
  Author: Samuele Mega
"""

import pickle
import json
import igraph as ig
import os

from helpers import communities_info

"""
  main
"""
if __name__ == "__main__":

  graph = ig.Graph.Read_Pickle("files/graph.pkl")

  with open(os.path.join("files", "communities_leiden.pkl"), "br") as file:
    communities_leiden = pickle.load(file)

  with open(os.path.join("files", "communities_louvain.pkl"), "br") as file:
    communities_louvain = pickle.load(file)

  with open(os.path.join("files", "communities_label_propagation.pkl"), "br") as file:
    communities_label_propagation = pickle.load(file)

  with open(os.path.join("files", "communities_leiden_analysis.json"), "w", encoding="utf-8") as file:
    json.dump(communities_info(graph, communities_leiden, 10), file, indent=2, ensure_ascii=False)

  print("[LOG] Analyzed: Leiden communities")

  with open(os.path.join("files", "communities_louvain_analysis.json"), "w", encoding="utf-8") as file:
    json.dump(communities_info(graph, communities_louvain, 10), file, indent=2, ensure_ascii=False)

  print("[LOG] Analyzed: Louvain communities")

  with open(os.path.join("files", "communities_label_propagation_analysis.json"), "w", encoding="utf-8") as file:
    json.dump(communities_info(graph, communities_label_propagation, 10), file, indent=2, ensure_ascii=False)

  print("[LOG] Analyzed: Label propagation communities")
