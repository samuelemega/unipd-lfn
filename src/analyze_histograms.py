"""
  Author: Samuele Mega
"""

import pickle
import json
import os
import matplotlib.pyplot as plt
import math

from helpers import communities_info

def plot(communities, label, filename):
  n = len(communities)

  magnitude = math.ceil(math.log(communities[0], 10))

  plt.clf()
  plt.bar(range(n), communities, color="skyblue", edgecolor="black", linewidth=0.5)
  plt.yscale("log")
  plt.xlabel("Community")
  plt.ylabel("Size")
  plt.title(f"Sizes of the communities ({label})")

  horizontal_lines = [10 ** i for i in range(magnitude)]

  for y in horizontal_lines:
    plt.hlines(y=y, xmin=-0.5, xmax=n-0.5, color="gray", linestyle="--", alpha=0.7, linewidth=0.5)

  plt.savefig(os.path.join("files", filename), format="png", dpi=300, bbox_inches="tight")

"""
  main
"""
if __name__ == "__main__":

  with open(os.path.join("files", "communities_leiden.pkl"), "br") as file:
    communities_leiden = pickle.load(file)

  with open(os.path.join("files", "communities_louvain.pkl"), "br") as file:
    communities_louvain = pickle.load(file)

  with open(os.path.join("files", "communities_label_propagation.pkl"), "br") as file:
    communities_label_propagation = pickle.load(file)

  communities_leiden_sizes = [
    len(c) for c in communities_leiden["communities"]
  ]

  communities_louvain_sizes = [
    len(c) for c in communities_louvain["communities"]
  ]

  communities_label_propagation_sizes = [
    len(c) for c in communities_label_propagation["communities"]
  ]

  n = 50

  communities_leiden_sizes = sorted(communities_leiden_sizes, reverse=True)[:n]
  communities_louvain_sizes = sorted(communities_louvain_sizes, reverse=True)[:n]
  communities_label_propagation_sizes = sorted(communities_label_propagation_sizes, reverse=True)[:n]

  plot(communities_leiden_sizes, "Leiden", "leiden.png")
  plot(communities_louvain_sizes, "Louvain", "louvain.png")
  plot(communities_label_propagation_sizes, "Label propagation", "label_propagation.png")

