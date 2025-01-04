import pickle
import igraph as ig

if __name__ == "__main__":

  with open("files/nodes.pkl", "br") as file:
    nodes = pickle.load(file)

  labels_indeces = { label: index for index, label in enumerate(list(nodes.keys())) }
  graph = ig.Graph(n=len(labels_indeces), directed=True)

  edges = []

  for label, node in nodes.items():
    parent_index = labels_indeces[label]
    for link in node["links"]:
      if link is not None:
        edges.append((parent_index, labels_indeces[link]))

  graph.add_edges(edges)

  for label, node in nodes.items():
    graph.vs[labels_indeces[label]]["label"] = label
    graph.vs[labels_indeces[label]]["categories"] = node["categories"]

  with open("files/graph.pkl", "wb") as file:
    pickle.dump(graph, file)
