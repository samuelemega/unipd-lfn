"""
  freq
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
"""
def pr_sort_vertices(graph, community):
  subgraph = graph.subgraph(community)
  scores = subgraph.pagerank()

  vertices = [(index, scores[index]) for index in range(len(scores))]

  vertices = sorted(vertices, key=lambda v: v[1], reverse=True)

  return vertices

"""
  community_categories
"""
def community_categories(graph, community):
  categories = []

  for item in community:
    categories += graph.vs[item]["categories"]

  return categories
