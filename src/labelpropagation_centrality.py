"""
  Author: Marco Facco
"""

import pickle
import igraph as ig
import numpy as np
from collections import Counter

def random_walk_centrality(subgraph, num_walks=1000, walk_length=50):
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
  central_node = max(centrality_scores, key=centrality_scores.get)
  return central_node, centrality_scores[central_node]


if __name__ == "__main__":
  # Load all saved subgraphs
  subgraphs = []
  i = 0
  while i != 10: # while True to compute all centralities 
    try:
      subgraphs.append(ig.Graph.Read_Pickle(f"src\\files\\subgraph{i}.pkl"))
      i += 1
    except FileNotFoundError:
      break
  print("Subgraphs loaded.")

  # Compute random walk centrality for each subgraph
  with open("src\\files\\subgraph_centrality.txt", "w", encoding="utf-8") as txt_file:
    for idx, subgraph in enumerate(subgraphs):
      try:
        central_node, centrality_score = random_walk_centrality(subgraph)
        # Save to text file
        txt_file.write(f"Subgraph {idx} central node: {central_node} with score: {centrality_score:.6f}\n")
        # Print to console
        print(f"Subgraph {idx} central node: {central_node} with score: {centrality_score:.6f}")

      except Exception as e:
        print(f"Error computing centrality for subgraph {idx}: {e}")

