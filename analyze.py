import igraph as ig

if __name__ == "__main__":
    g=ig.Graph.Read_Pickle("src\\files\\graph.pkl")
    ug= g.as_undirected()
    com=ig.Graph.community_multilevel(ug)
    nNodes=ug.vcount()
    subcoms=com.subgraphs()
    with open("src\\files\\res.txt", "w") as f:
      i=0
      d=0
      for sub in subcoms:
        sNodes=sub.vcount()
        sRatio=sNodes/nNodes*100
        print("dimension of cluster",repr(i),":", repr(sRatio),file=f)
        d+=sub.average_path_length(directed=False)
        i+=1
      print("avg intra-cluster distance:", repr(d/i),file=f)
    with open("src\\files\\res.txt","w") as f:
      print("louvain modularity score:",repr(com.modularity),file=f)
    #ig.plot(ug,"prova.pdf")
    
      
