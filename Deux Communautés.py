import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import Counter


N=100


#Premier cas: chaque agent a sa propre devise



'''On reprend les fonctions précédentes, et on modifie 
seulement la manière de construire le graphe, de telle 
sorte à ce qu'il y ait deux communautés ayant une 
probabilité pinter de connection entre deux noeuds de la 
même communauté, et une proba pintra de connection entre 
deux noeuds de communautés différentes (On considère 
que les N/2 premiers noeuds appartiennent à une 
communauté, et que le reste appartient à l'autre 
communauté)'''



#Fonction changement de devise lorsque les connections de i utilisent majoritairement une autre devise 


def change_currency(i,G):
    '''Cette fonction modifie la devise de i en la devise la plus
    utilisée par ses connections.
    Si plusieurs devises sont utilisées par le même nombre maximal 
    de voisins, on choisit aléatoirement l'une de ces devises 
    (en donnant la priorité à la devise utilisée par i).

    Args:
        i(integer): Le noeud considéré
        G(Graph):Le graphe représentant les connections des différents agents

    Returns:
        Ne retourne rien, modifie la devise de i si nécessaire
    '''


    neighbors=list(G.neighbors(i))
    if neighbors:
        d=Counter([G.nodes[j]['currency'] for j in neighbors])
        currency_max=max(d,key=d.get)
        if G.nodes[i]['currency']!=currency_max:
            count_max=max(d.values())
            currencies_max=[j for j,s in d.items() if s==count_max]
            if G.nodes[i]['currency'] in currencies_max:
                currency=G.nodes[i]['currency']
            else:
                currency=random.choice(currencies_max)
            G.nodes[i]['currency']=currency






#La fonction qui retourne l'utilité sociale à partir d'un graphe

def social_utility(G):
    '''Cette fonction soustrait une unité pour chaque couple de 
    noeud ne possédant pas la même devise. le but est donc de 
    maxisimer cette fonction afin d'optimiser les échanges.
    À chaque changement de devise d'un des agents, cette fonction 
    retourne un entier relatif strictement supérieur au précédent.
    C'est pourquoi il faut s'arrêter lorsque l'entier retourné 
    est le même que le précédent.
    Args:
        G(Graph)
    Returns:
        Retourne l'utilité sociale
    '''

    u=0
    for node1,node2 in G.edges():
        if G.nodes[node1]['currency']!=G.nodes[node2]['currency']:
            u=u-1
    return u




#La fonction qui retourne le nombre de devises dans le système final

def currencies_number(G):
    '''Cette fonction parcours tous les noeuds de G et change leur
    devise si nécessaire grâce à la fonction change_currency.
    Cette opération est répétée tant que l'utilité sociale diminue.
    Lorsque celle-ci est constante, le système est optimal. 
    La fonction retourne alors le nombre de devises distinctes 
    dans le graphe G
    Args:
        G(Graph)
    Returns:
        Le nombre de devises dans le graphe
    '''

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


#Test des fonctions pour le cas de deux communautés


pinter=0.3
pintra=0.05
B=nx.Graph() 
B.add_nodes_from(range(1,N+1)) 

for i in range(1,N+1):
    B.nodes[i]['currency']=str(i)

for i in range(1,(N//2)+1):
    for j in range(i+1,(N//2)+1):
        if random.random()<pinter:
            B.add_edge(i, j)
    for j in range((N//2)+1,N+1):
        if random.random()<pintra:
            B.add_edge(i,j)
for i in range((N//2)+1,N+1):
    for j in range(i+1,N+1):
        if random.random()<pinter:
            B.add_edge(i,j)

print("B:",B)
print("L'utilité sociale de B est",social_utility(B))
print("Le nombre de devises dans B est",currencies_number(B))

L=set(B.nodes[i]['currency'] for i in B.nodes())

print("Les devises dans le système final sont:",L)


