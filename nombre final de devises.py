import random
import matplotlib.pyplot as plt
import networkx as nx



s=0
p=0.05
N=100

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

print(s/10000) #Moyenne des devises à l'état final