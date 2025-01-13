from helpers import weighted_soergel, fr_sort_categories, pr_sort_vertices, community_categories

"""
  mean_weighted_soergel_communities_distance
"""
def mean_weighted_soergel_communities_distance(graph, communities):
  total = 0
  count = 0

  print("start")

  for i in range(len(communities)):
    for j in range(len(communities)):
      if i != j:
        count += 1
        total += weighted_soergel(
          community_categories(graph, communities[i]),
          community_categories(graph, communities[j]),
        )
    print(f"\r{i}", end="")

  print(len(communities) ** 2- len(communities))
  print(count)

  return total / (len(communities) ** 2 - len(communities))

"""
  communities_info
"""
def communities_info(graph, communities, n):
  modularity = communities["modularity"]
  communities = sorted(communities["communities"], key=len, reverse=True)[:30]

  return {
    "graph": {
      "count": graph.vcount(),
      "communities": len(communities),
      "soergel": mean_weighted_soergel_communities_distance(graph, communities),
      "modularity": modularity,
    },
    "communities": [{
      "count": len(c),
      "dimension": round(len(c) / graph.vcount() * 100, 3),
      "categories": [
        category[0]
        for category in fr_sort_categories(graph, c)[:n]
      ],
      "vertices": [
        graph.vs[v[0]]["label"]
        for v in pr_sort_vertices(graph, c)[:n]
      ]
    } for c in communities]
  }
