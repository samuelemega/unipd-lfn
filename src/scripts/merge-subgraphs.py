import os
import json
from collections import deque

subgraphs_folder = "../subgraphs"

"""
    merge_subgraphs
"""
def merge_subgraphs(
    graph_pages,
    subgraph_1_index,
    subgraph_2_index,
    subgraph_1_edges,
    subgraph_2_edges
):
    index = 0

    subgraph_3_index = {}
    subgraph_3_edges = {}

    subgraph_1_index_keys = subgraph_1_index.keys()
    subgraph_2_index_keys = subgraph_2_index.keys()

    subgraph_1_edges_keys = subgraph_1_edges.keys()
    subgraph_2_edges_keys = subgraph_2_edges.keys()

    subgraph_1_index_inverse = { f"{value}": key for key, value in subgraph_1_index.items() }
    subgraph_2_index_inverse = { f"{value}": key for key, value in subgraph_2_index.items() }

    # - Merging the indexes

    for subgraph_1_page_title in subgraph_1_index_keys:
        if subgraph_1_page_title in graph_pages and subgraph_1_page_title not in subgraph_3_index:
            subgraph_3_index[subgraph_1_page_title] = index
            index += 1

    for subgraph_2_page_title in subgraph_2_index_keys:
        if subgraph_2_page_title in graph_pages and subgraph_2_page_title not in subgraph_3_index:
            subgraph_3_index[subgraph_2_page_title] = index
            index += 1

    # - Merging the edges

    for subgraph_1_page_index in subgraph_1_edges_keys:
        subgraph_1_page_title = subgraph_1_index_inverse[f"{subgraph_1_page_index}"]
        subgraph_3_page_index = subgraph_3_index[subgraph_1_page_title]

        for subgraph_1_childpage_index in subgraph_1_edges[subgraph_1_page_index]:
            subgraph_1_childpage_title = subgraph_1_index_inverse[f"{subgraph_1_childpage_index}"]

            if subgraph_1_childpage_title in subgraph_3_index:
                subgraph_3_childpage_index = subgraph_3_index[subgraph_1_childpage_title]

                if subgraph_3_page_index not in subgraph_3_edges:
                    subgraph_3_edges[subgraph_3_page_index] = set()

                subgraph_3_edges[subgraph_3_page_index].add(subgraph_3_childpage_index)

    for subgraph_2_page_index in subgraph_2_edges_keys:
        subgraph_2_page_title = subgraph_2_index_inverse[f"{subgraph_2_page_index}"]
        subgraph_3_page_index = subgraph_3_index[subgraph_2_page_title]

        for subgraph_2_childpage_index in subgraph_2_edges[subgraph_2_page_index]:
            subgraph_2_childpage_title = subgraph_2_index_inverse[f"{subgraph_2_childpage_index}"]

            if subgraph_2_childpage_title in subgraph_3_index:
                subgraph_3_childpage_index = subgraph_3_index[subgraph_2_childpage_title]

                if subgraph_3_page_index not in subgraph_3_edges:
                    subgraph_3_edges[subgraph_3_page_index] = set()

                subgraph_3_edges[subgraph_3_page_index].add(subgraph_3_childpage_index)

    return subgraph_3_index, subgraph_3_edges

"""
    load_index_file
"""
def load_index_file(dump_number):
    index = {}

    print(f"[LOG] Loading dump-{dump_number}-index")

    with open(os.path.join(subgraphs_folder, f"dump-{dump_number}-index"), "r") as json_file:
        index = json.load(json_file)

    return index

"""
   load_edges_file
"""
def load_edges_file(dump_number):
    edges = {}

    print(f"[LOG] Loading dump-{dump_number}-edges")

    with open(os.path.join(subgraphs_folder, f"dump-{dump_number}-edges"), "r") as json_file:
        edges = json.load(json_file)

    edges = { key: set(value) for key, value in edges.items() }

    return edges

"""
   load_pages_file
"""
def load_pages_file(dump_number):
    pages = None

    print(f"[LOG] Loading dump-{dump_number}-pages")

    with open(os.path.join(subgraphs_folder, f"dump-{dump_number}-pages"), "r") as json_file:
        pages = json.load(json_file)

    pages = set(pages)

    return pages

"""
    main
"""

if __name__ == "__main__":

    # - Merging graph pages

    graph_pages = [
        load_pages_file(dump_number) for dump_number in range(1, 96)
    ]

    graph_pages = set({ x for _set in graph_pages for x in _set })

    # - Queueing tasks

    subgraphs = deque([
        (load_index_file(dump_number), load_edges_file(dump_number)) for dump_number in range(1, 96)
    ])

    while len(subgraphs) > 1:
        subgraph_1_index, subgraph_1_edges = subgraphs.popleft()
        subgraph_2_index, subgraph_2_edges = subgraphs.popleft()

        subgraphs.append(merge_subgraphs(
            graph_pages,
            subgraph_1_index,
            subgraph_2_index,
            subgraph_1_edges,
            subgraph_2_edges,
        ))

        print(f"Remaining: {len(subgraphs)}")

    graph_index, graph_edges = subgraphs.pop()

    graph_edges = { key: list(value) for key, value in graph_edges.items() }

    with open(os.path.join("./output", "graph-index"), "w", encoding="utf-8") as json_file:
        json.dump(graph_index, json_file, indent=2, ensure_ascii=False)

    with open(os.path.join("./output", "graph-edges"), "w", encoding="utf-8") as json_file:
        json.dump(graph_edges, json_file, indent=2, ensure_ascii=False)
