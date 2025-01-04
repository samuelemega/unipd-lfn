import pickle

if __name__ == "__main__":
  with open("output/graph.pkl", "br") as file:
    graph = pickle.load(file)
