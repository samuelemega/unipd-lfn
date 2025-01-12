import pickle
import igraph as ig

import pickle
import igraph as ig

if __name__ == "__main__":
    g = ig.Graph.Read_Pickle("src\\files\\graph.pkl")
    ug = g.as_undirected()

    # Detect communities using the Label Propagation algorithm
    com = ug.community_label_propagation()
    num_nodes = ug.vcount()
    subcoms = com.subgraphs()
    i = 0

    for sub in subcoms:
        with open("src\\files\\subgraph" + repr(i) + ".pkl", "wb") as file:
            sRatio = sub.vcount() / num_nodes
            pickle.dump(sub, file)
        i += 1