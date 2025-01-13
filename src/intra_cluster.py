"""
  Author: Federico Cognolatto
"""

import igraph as ig


def communities_avg_intra_cluster_distance(communities):
  with open("src\\files\\res.txt", "w") as f:
    i=0
    d=0
    for sub in communities:
      d+=sub.average_path_length(directed=False)
      i+=1
    print("avg intra-cluster distance:", repr(d/i),file=f)
