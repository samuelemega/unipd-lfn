import leidenalg as la

"""
  compute_communities_modularity_vertex
"""
def compute_communities_modularity_vertex(graph):
  partition = la.find_partition(graph, la.ModularityVertexPartition)
  lst = [item for item in partition]

  return {
    "communities": lst,
    "modularity": partition.modularity,
  }

"""
  compute_communities_significance_vertex
"""
def compute_communities_significance_vertex(graph):
  partition = la.find_partition(graph, la.SignificanceVertexPartition)
  lst = [item for item in partition]

  return {
    "communities": lst,
    "modularity": partition.modularity,
  }
