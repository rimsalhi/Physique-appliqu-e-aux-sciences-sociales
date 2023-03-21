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
    if neighbors==[]:
        pass
    else:
        d={}
        for j in neighbors:
            if G.nodes[j]['currency'] not in d:
                d[G.nodes[j]['currency']]=1
            else:
                d[G.nodes[j]['currency']]+=1
        max1=max(d.values())
        L=[j for j,v in d.items() if v==max1]
        if G.nodes[i]['currency'] in d and d[G.nodes[i]['currency']]==max1:
            pass
        else:
            G.nodes[i]['currency']=random.choice(L)


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

