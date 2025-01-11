import pickle

import igraph as ig

if __name__ == "__main__":
    g=ig.Graph.Read_Pickle("src\\files\\graph.pkl")
    ug= g.as_undirected()
    com=ig.Graph.community_multilevel(ug)
    nNodes=ug.vcount()
    subcoms=com.subgraphs()
    i=0
    for sub in subcoms:
      with open("src\\files\\subgraph"+repr(i)+".pkl", "wb") as file:
        sRatio=sub.vcount/nNodes
        print("intra-cluster distance:", repr(sub.average_path_length(directed=False)))
        pickle.dump(sub,file)
      i+=1
    with open("src\\files\\modularity.txt","w") as f:
      print("louvain modularity score:",repr(com.modularity),file=f)
    ig.plot(ug,"prova.pdf")
    
      
