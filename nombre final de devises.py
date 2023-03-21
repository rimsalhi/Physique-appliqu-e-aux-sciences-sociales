import random
import matplotlib.pyplot as plt
import networkx as nx

N=100

#la fonction social_utility retourne l'utilité sociale du système 
def social_utility(G):
    u=0
    for node1,node2 in G.edges():
        if G.nodes[node1]['currency']!=G.nodes[node2]['currency']:
            u=u-1
    return u


#Étant donné une probabilité p, on calcule le nombre de devises distinctes dans le système final
#Tant que l'utilité sociale change, il faut parcourir à nouveau tous les noeuds du graphe
def currencies_number(G):
    u=social_utility(G)
    precedent=None
    while u!=precedent:
        precedent=u
        for i in G.nodes():
            change_currency(i,G)
        u=social_utility(G)
    L=[]
    for i in G.nodes:
        if G.nodes[i]['currency'] not in L:
            L.append(G.nodes[i]['currency'])
    return len(L)
        


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