"""
  Author: Samuele Mega
"""

import pickle

if __name__ == "__main__":
  toc = {}

  with open("files/dump-index.txt", "r", encoding="utf-8") as file:
    for line in file:
      [offset, id, title] = line.rstrip('\n').split(":", 2)
      toc[title] = offset

  with open("files/toc.pkl", "wb") as file:
    pickle.dump(toc, file)
