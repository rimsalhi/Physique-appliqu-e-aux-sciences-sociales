import random
import matplotlib.pyplot as plt
import networkx as nx

N=100
p=0.05

G=nx.Graph()  #Graphe vide

G.add_nodes_from(range(1,N+1))

for i in range(1,N+1):
    G.nodes[i]['currency']='i'

for i in range(N):
    for j in range(i+1,N):
        if random.random()<=p:
            G.add_edge(i, j)



options={
    'node_color':'green',
    'edge_color':'grey',
    'with_labels':True
    }
plt.figure()
nx.draw(G,**options)
plt.show()
