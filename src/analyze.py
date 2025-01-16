"""
  Author: Samuele Mega
"""

import pickle
import json
import igraph as ig
import os
import leidenalg as la

def compute_rai_index(partitions):
  n = len(partitions)
  sum = 0
  count = 0

  for i in range(n):
    for j in range(n):
      if i != j:
        sum += ig.compare_communities(partitions[i], partitions[j], method="adjusted_rand")
        count += 1

  return sum / count


"""
  main
"""
if __name__ == "__main__":

  graph = ig.Graph.Read_Pickle("files/graph.pkl")
  undirected_graph = graph.as_undirected()

  n = 5

  partitions_leiden = []
  partitions_louvain = []
  partitions_label_propagation = []

  for i in range(n):
    partitions_leiden.append(la.find_partition(graph, la.ModularityVertexPartition))
    print(f"[LOG] Computed partition {i + 1} (Leiden)")

  for i in range(n):
    partitions_louvain.append(ig.Graph.community_multilevel(undirected_graph))
    print(f"[LOG] Computed partition {i + 1} (Louvain)")

  for i in range(n):
    partitions_label_propagation.append(undirected_graph.community_label_propagation())
    print(f"[LOG] Computed partition {i + 1} (Label propagation)")

  leiden_rai_index = compute_rai_index(partitions_leiden)
  louvain_rai_index = compute_rai_index(partitions_louvain)
  label_propagation_rai_index = compute_rai_index(partitions_label_propagation)

  print(f"Leiden RAI Index: {leiden_rai_index}")
  print(f"Louvain RAI Index: {louvain_rai_index}")
  print(f"Label propagation RAI Index: {label_propagation_rai_index}")

"""
  Leiden RAI Index: 0.651396256018093
  Louvain RAI Index: 0.5794245161426191
  Label propagation RAI Index: 0.7026209560215031
"""
