
def mean_currencies(G,p):
    s=0
    for i in range(10000):

        G=nx.Graph() 

        G.add_nodes_from(range(1,N+1)) 

        for i in range(1,N+1):
            G.nodes[i]['currency']=str(i)

        for i in range(1,N+1):
            for j in range(i+1,N+1):
                if random.random()<p:
                    G.add_edge(i, j)
           

    s+=currencies_number(G)

    return(s/10000)


