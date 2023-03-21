import random
import matplotlib.pyplot as plt
import networkx as nx

N=100
p=0.05

G=nx.Graph()

G.add_nodes_from(range(N))

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
