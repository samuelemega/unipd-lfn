import os
import py7zr
import mwxml
import re
import json
from concurrent.futures import ThreadPoolExecutor

regex = re.compile(r'\[\[([^\|\]]+)(?:\|[^\]]*)?\]\]')

dumps_folder = "../../dumps"
extracted_folder = "../../extracted"
subgraphs_folder = "../../subgraphs"

file_names = [f"dump-{dump_index}" for dump_index in range(1, 96)]

"""
    normalize_string
"""
def normalize_string(value):
    value = value.strip().strip("_")

    if len(value) == 0:
        return None

    value = value[0].upper() + value[1:]
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"_+", "_", value)

    return value

"""
    check_file_existence
"""
def check_file_existence(folder, file_name):
    file_path = os.path.join(folder, file_name)

    return os.path.exists(file_path)

"""
    remove_file
"""
def remove_file(folder, file_name):
    file_path = os.path.join(folder, file_name)

    os.remove(file_path)

    print(f"[LOG] Deleting: {file_name}")

"""
    extract_file
"""
def extract_file(src_folder, dst_folder, file_name):
    src_file_path = os.path.abspath(os.path.join(src_folder, file_name + ".7z"))
    dst_folder_path = os.path.abspath(dst_folder)

    os.makedirs(dst_folder_path, exist_ok=True)

    with py7zr.SevenZipFile(src_file_path, mode="r") as archive:
        print(f"[LOG] Extracting: {file_name}")

        file_names = archive.getnames()

        archive.extractall(path=dst_folder_path)

    print(f"[LOG] Extracted: {file_name}")

"""
    compute_subgraph
"""
def compute_subgraph(folder, file_name):
    file_path = os.path.join(folder, file_name)

    dump = mwxml.Dump.from_file(open(file_path))

    # - Computing the map of index

    print(f"[LOG] Indexing: {file_name}")

    index = 0

    subgraph_index = {}
    subgraph_edges = {}
    subgraph_pages = set()

    for page in dump:
        page_title_normalized = normalize_string(page.title)

        if page_title_normalized is not None:
            subgraph_pages.add(page_title_normalized)

            if page_title_normalized not in subgraph_index:
                subgraph_index[page_title_normalized] = index
                index += 1

            if subgraph_index[page_title_normalized] not in subgraph_edges:
                subgraph_edges[subgraph_index[page_title_normalized]] = set()

            last_revision = None

            for revision in page:
                if revision.text:
                    last_revision = revision

            if last_revision is not None:
                for match in regex.findall(last_revision.text):
                    match_normalized = normalize_string(match)

                    if match_normalized is not None:
                        if match_normalized not in subgraph_index:
                            subgraph_index[match_normalized] = index
                            index += 1

                        subgraph_edges[subgraph_index[page_title_normalized]].add(subgraph_index[match_normalized])

    print(f"[LOG] Indexed: {file_name}")

    return subgraph_index, subgraph_edges, subgraph_pages

"""
    print_index
"""
def print_index(folder, file_name, index):
    with open(os.path.join(folder, f"{file_name}-index"), "w", encoding="utf-8") as json_file:
        json.dump(index, json_file, indent=1, ensure_ascii=False)

"""
    print_edges
"""
def print_edges(folder, file_name, edges):
    edges = { int(key): list(value) for key, value in edges.items() }

    with open(os.path.join(folder, f"{file_name}-edges"), "w", encoding="utf-8") as json_file:
        json.dump(edges, json_file, indent=1, ensure_ascii=False)

"""
    print_pages
"""
def print_pages(folder, file_name, pages):
    pages = list(pages)

    with open(os.path.join(folder, f"{file_name}-pages"), "w", encoding="utf-8") as json_file:
        json.dump(pages, json_file, indent=1, ensure_ascii=False)

"""
    compute
"""
def compute(file_name):
    if not check_file_existence(subgraphs_folder, file_name):
        extract_file(dumps_folder, extracted_folder, file_name)

        subgraph_index, subgraph_edges, subgraph_pages = compute_subgraph(extracted_folder, file_name)

        print_index(subgraphs_folder, file_name, subgraph_index)
        print_edges(subgraphs_folder, file_name, subgraph_edges)
        print_pages(subgraphs_folder, file_name, subgraph_pages)

        remove_file(extracted_folder, file_name)

"""
    main
"""
if __name__ == "__main__":
    os.makedirs(subgraphs_folder, exist_ok=True)

    with ThreadPoolExecutor(max_workers=2) as executor:
        for file_name in file_names:
            executor.submit(compute,file_name)
