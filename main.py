import random
import matplotlib.pyplot as plt
import networkx as nx



N=100 #Nombre d'agents




''' Comment fonctionne la librairie networkx '''

#Construction d'un graphe grâce à la librairie networkx

#graphe vide
G=nx.Graph() 

#Ajout des noeuds (agents)
G.add_nodes_from(range(1,N+1)) 

#Au départ, chaque individu i utilise une devise 'i'
for i in range(1,N+1):
    G.nodes[i]['currency']=str(i)

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



'''Fonction changement de devise lorsque les connections 
de i utilisent majoritairement une autre devise '''


