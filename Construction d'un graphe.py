import random
import matplotlib.pyplot as plt
import networkx as nx

N=100
p=0.05

#Graphe vide
G=nx.Graph() 


#Ajout des sommets (agents)
G.add_nodes_from(range(1,N+1)) 


#Au départ, chaque individu i utilise une devise 'i'
for i in range(1,N+1):
    G.nodes[i]['currency']='i'



#On ajoute des arêtes avec une probabilité p 
for i in range(1,N+1):
    for j in range(i+1,N+1):
        if random.random()<p:
            G.add_edge(i, j)


#Affichage du graphe
options={
    'node_color':'green',
    'edge_color':'grey',
    'with_labels':True
    }
plt.figure()
nx.draw(G,**options)
plt.show()
