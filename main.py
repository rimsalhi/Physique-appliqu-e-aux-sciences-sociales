import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np



N=100 #Nombre d'agents




''' Comment fonctionne la librairie networkx 

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
'''




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



#Test des fonctions définies précédemment

p=0.05
B=nx.Graph() 
B.add_nodes_from(range(1,N+1)) 

for i in range(1,N+1):
    B.nodes[i]['currency']=str(i)

for i in range(1,N+1):
    for j in range(i+1,N+1):
        if random.random()<p:
            B.add_edge(i, j)

print("B:",B)
print("L'utilité sociale de B est",social_utility(B))
print("Le nombre de devises dans B est",currencies_number(B))

L=[]
for i in B.nodes:
    if B.nodes[i]['currency'] not in L:
        L.append(B.nodes[i]['currency'])
    

print("Les devises dans le système final sont:",L)


#La fonction qui retourne la moyenne sur 10000 systèmes des nombres de devises à l'état final

def mean_currencies(p):
    '''Cette fonction ajoute à chaque étape le nombre de devises 
    à l'état final d'un graphe aléatoire avec une probabilité p
    de connection entre deux noeuds, puis divise par le nombre 
    de graphes considérés (10000 dans ce cas) afin d'avoir une 
    moyenne.

    Args:
        p(float): Probabilité de connection entre deux noeuds
    
    Returns:
        La moyenne des nombres de devises à l'état final
    '''

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



#Tests de cette fonction

print("La moyenne pour p=0.1 est égale à",mean_currencies(0.1))
print("La moyenne pour p=0.1 est égale à",mean_currencies(0.05))
print("La moyenne pour p=0.1 est égale à",mean_currencies(0.5))
print("La moyenne pour p=0.1 est égale à",mean_currencies(0.8))



''' On remarque que pour p>0.1, cette moyenne est égale à 1. 
Intuitivement, plus les agents sont connectés, plus ils sont
amenés à avoir une seule devise commune. De façon analogue, lorsque 
p tend vers 0, la moyenne tend vers 100'''


#On trace les résultats pour plusieurs valeurs de p 

P=np.linspace(0,1,100)
M=[]
for p in P:
    M.append(mean_currencies(p))

plt.plot(P,M)
plt.show() #Complexité élevée, prend trop de tps à être executé
'''Plus p tend vers 0, plus la moyenne tend vers 100.
Inversement, plus p tend vers 1, plus la moyenne tend vers 1'''



