import numpy as np
from collections import Counter

"""
  freq

  Author: Samuele Mega
"""
def freq(lst):

  if len(lst) == 0:
    return {}

  items = {}
  unit = 1 / len(lst)

  for i in lst:
    if i not in items:
      items[i] = unit
    else:
      items[i] += unit

  return items

"""
  weighted_soergel

  Author: Samuele Mega
"""
def weighted_soergel(lst_a, lst_b):
  items = set(lst_a) | set(lst_b)
  freq_a = freq(lst_a)
  freq_b = freq(lst_b)

  inter = sum([min(freq_a.get(i, 0), freq_b.get(i, 0)) for i in items])
  union = sum([max(freq_a.get(i, 0), freq_b.get(i, 0)) for i in items])

  return 1 - inter / union

"""
  fr_sort_categories

  Author: Samuele Mega
"""
def fr_sort_categories(graph, community):
  categories = {}
  count = 0

  for i in community:
    for c in graph.vs[i]["categories"]:
      count += 1
      if c not in categories:
        categories[c] = 0
      else:
        categories[c] += 1

  categories = { key: value / count for key, value in categories.items() }

  categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)

  return categories

"""
  pr_sort_vertices

  Author: Samuele Mega
"""
def pr_sort_vertices(graph, community):
  subgraph = graph.subgraph(community)
  scores = subgraph.pagerank()

  vertices = [(index, scores[index]) for index in range(len(scores))]

  vertices = sorted(vertices, key=lambda v: v[1], reverse=True)

  return [subgraph.vs[v[0]]["label"] for v in vertices]

"""
  community_categories

  Author: Samuele Mega
"""
def community_categories(graph, community):
  categories = []

  for item in community:
    categories += graph.vs[item]["categories"]

  return categories

"""
  mean_weighted_soergel_communities_distance

  Author: Samuele Mega
"""
def mean_weighted_soergel_communities_distance(graph, communities):
  total = 0
  count = 0

  for i in range(len(communities)):
    for j in range(len(communities)):
      if i != j:
        count += 1
        total += weighted_soergel(
          community_categories(graph, communities[i]),
          community_categories(graph, communities[j]),
        )
    print(f"\rWeighted Soergel analysis: {i + 1} / {len(communities)}", end="")
  print()

  return total / count

"""
  community_info

  Author: Samuele Mega
"""
def community_info(graph, community, n):
  return {
    "count": len(community),
    "dimension": round(len(community) / graph.vcount() * 100, 3),
    "categories": [c[0] for c in fr_sort_categories(graph, community)[:n]],
    "page_rank_centers": pr_sort_vertices(graph, community)[:n],
    "random_walk_center": random_walk_centrality(graph, community)[:n],
  }

"""
  communities_info

  Author: Samuele Mega
"""
def communities_info(graph, communities, n):
  modularity = communities["modularity"]
  duration = communities["duration"]

  main_communities = sorted(communities["communities"], key=len, reverse=True)[:30]
  communities_sizes = [len(community) for community in communities["communities"]]

  return {
    "info": {
      "vertices_count": graph.vcount(),
      "edges_count": graph.ecount(),
      "algotithm_duration": duration,
    },
    "communities_statistics": {
      "mean_modularity": modularity,
      "mean_soergel": mean_weighted_soergel_communities_distance(graph, main_communities),
      "count": len(communities["communities"]),
      "mean": float(np.mean(communities_sizes)),
      "median": float(np.median(communities_sizes)),
      "iqr": float(np.percentile(communities_sizes, 75) - np.percentile(communities_sizes, 25)),
      "giant_component": int(np.max(communities_sizes)),
    },
    "communities": [community_info(graph, c, n) for c in main_communities],
  }

"""
  communities_avg_intra_cluster_distance

  Author: Federico Cognolatto
"""
def communities_avg_intra_cluster_distance(communities):
  dist = 0

  for community in communities:
    dist += community.average_path_length(directed=False)

  return dist / len(communities)

"""
  random_walk_centrality

  Author: Marco Facco
"""
def random_walk_centrality(graph, community, num_walks=1000, walk_length=50):
  subgraph = graph.subgraph(community)

  """
    Compute the central node of a subgraph, where the centrality score is computed using random walks.
    Returns a tuple containing the label of the node with the highest centrality and its score.
    """
  visited_nodes = []
  for _ in range(num_walks):
    start_vertex = np.random.randint(0, subgraph.vcount())  # Random starting node
    walk = subgraph.random_walk(start=start_vertex, steps=walk_length)
    visited_nodes.extend(walk)

  # Count visits for each node
  visit_counts = Counter(visited_nodes)

  # Normalize centrality scores
  total_visits = sum(visit_counts.values())
  centrality_scores = {subgraph.vs[node]["label"]: visit_counts[node] / total_visits for node in visit_counts}

  # Find the node with the highest centrality

  vertices = sorted(centrality_scores.items(), key=lambda item: item[1], reverse=True)

  return [v[0] for v in vertices]
