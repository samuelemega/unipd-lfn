"""
  Author: Samuele Mega, Marco Facco, Federico Cognolatto
"""

import igraph as ig
import pickle
import os
import time
import leidenalg as la

if __name__ == "__main__":
  graph = ig.Graph.Read_Pickle(os.path.join("files", "graph.pkl"))
  undirected_graph = graph.as_undirected()

  with open(os.path.join("files", "communities_leiden.pkl"), "wb") as file:
    start_time = time.time()
    partition = la.find_partition(graph, la.ModularityVertexPartition)
    end_time = time.time()

    lst = [item for item in partition]

    pickle.dump({
      "communities": lst,
      "modularity": partition.modularity,
      "duration": end_time - start_time,
    }, file)

  print("[LOG] Generated: Leiden communities")

  with open(os.path.join("files", "communities_louvain.pkl"), "wb") as file:
    start_time = time.time()
    partition = ig.Graph.community_multilevel(undirected_graph)
    end_time = time.time()

    lst = [item for item in partition]

    pickle.dump({
      "communities": lst,
      "modularity": partition.modularity,
      "duration": end_time - start_time,
    }, file)

  print("[LOG] Generated: Louvain communities")

  with open(os.path.join("files", "communities_label_propagation.pkl"), "wb") as file:
    start_time = time.time()
    partition = undirected_graph.community_label_propagation()
    end_time = time.time()

    lst = [item for item in partition]

    pickle.dump({
      "communities": lst,
      "modularity": partition.modularity,
      "duration": end_time - start_time,
    }, file)

  print("[LOG] Generated: Label propagation communities)")
