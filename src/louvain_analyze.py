"""
  Author: Federico Cognolatto
"""

import time
import igraph as ig
import os

from intra_cluster import communities_avg_intra_cluster_distance

if __name__ == "__main__":
  g=ig.Graph.Read_Pickle("src\\files\\graph.pkl")
  ug= g.as_undirected()
  startTime=time.time()
  com=ig.Graph.community_multilevel(ug)
  endTime=time.time()-startTime
  with open(os.path.join("files", "res.txt"), "w") as f:
    print("louvain time execution in seconds:",repr(endTime),file=f)
    print("louvain modularity score:",repr(com.modularity),file=f)
  communities=com.subgraphs()
  communities_avg_intra_cluster_distance(communities)
