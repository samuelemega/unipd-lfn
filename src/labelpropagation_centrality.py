"""
  Author: Marco Facco
"""

import igraph as ig
import os

if __name__ == "__main__":
  # Load all saved subgraphs
  subgraphs = []
  i = 0
  while i != 10: # while True to compute all centralities
    try:
      subgraphs.append(ig.Graph.Read_Pickle(os.path.join("files", f"subgraph{i}.pkl")))
      i += 1
    except FileNotFoundError:
      break
  print("Subgraphs loaded.")

  # Compute random walk centrality for each subgraph
  with open(os.path.join("files", "subgraph_centrality.txt"), "w", encoding="utf-8") as txt_file:
    for idx, subgraph in enumerate(subgraphs):
      try:
        central_node, centrality_score = random_walk_centrality(subgraph)
        # Save to text file
        txt_file.write(f"Subgraph {idx} central node: {central_node} with score: {centrality_score:.6f}\n")
        # Print to console
        print(f"Subgraph {idx} central node: {central_node} with score: {centrality_score:.6f}")

      except Exception as e:
        print(f"Error computing centrality for subgraph {idx}: {e}")
