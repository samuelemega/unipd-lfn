import os
import json
from igraph import Graph

graph_folder = "../../graph"

if __name__ == "__main__":
    with open(os.path.join(graph_folder, f"graph-index"), "r") as json_file:
        index = json.load(json_file)

    with open(os.path.join(graph_folder, f"graph-edges"), "r") as json_file:
        edges = json.load(json_file)

    g = Graph(n=len(index), directed=True)

    print("[LOG] Computing edges")

    edges_computed = [(int(page_index), childpage_index) for page_index, page_edges in edges.items() for childpage_index in page_edges]

    print("[LOG] Adding nodes")

    for page_title, page_index in index.items():
        g.vs[page_index]["label"] = page_title

    print("[LOG] Adding edges")

    g.add_edges(edges_computed)

    print("[LOG] Computing")

    density = g.density()
    print("Densità del grafo:", density)
