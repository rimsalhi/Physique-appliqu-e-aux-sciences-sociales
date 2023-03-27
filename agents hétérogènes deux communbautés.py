import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import Counter
'''On reprend les mêmes simulations que précédemment mais en ajoutant l'impact d'agents hétérogènes'''

N=100


#Premier cas: chaque agent a sa propre devise



'''On reprend les fonctions précédentes, et on modifie 
seulement la manière de construire le graphe, de telle 
sorte à ce qu'il y ait deux communautés ayant une 
probabilité pintra de connexion entre deux noeuds de la 
même communauté, et une proba pinter de connexion entre 
deux noeuds de communautés différentes (On considère 
que les N/2 premiers noeuds appartiennent à une 
communauté, et que le reste appartient à l'autre 
communauté)'''



#Fonction changement de devise lorsque les connexions de i utilisent majoritairement une autre devise 


def change_currency(i,G):
    '''Cette fonction modifie la devise de i en la devise la plus
    utilisée par ses connexions.
    Si plusieurs devises sont utilisées par le même nombre maximal 
    de voisins, on choisit aléatoirement l'une de ces devises 
    (en donnant la priorité à la devise utilisée par i).

    Args:
        i(integer): Le noeud considéré
        G(Graph):Le graphe représentant les connexions des différents agents

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

def social_utility_hetero(G):
    '''Cette fonction calcule l'utilité sociale dans le cas d'agents hétérogènes.
    On suppose que chaque agent j a une ponderation  pj égale à son degré (nombre  de voisins).
    Ainsi lorsque i veut échanger avec j, il doit payer pi si les monnaies de i et de j sont différentes.
    Le but est donc de maxisimer cette fonction afin d'optimiser les échanges.
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
    for node1 in G.nodes():
        for node2 in G.nodes():
            deg=len(list(G.neighbors(node1))) #impact des agents hétérogènes
            if G.nodes[node1]['currency']!=G.nodes[node2]['currency']:
                u=u-deg
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

    u=social_utility_hetero(G)
    precedent=None
    while u!=precedent:
        precedent=u
        for i in G.nodes():
            change_currency(i,G)
        u=social_utility_hetero(G)
    L=[]
    for i in G.nodes:
        if G.nodes[i]['currency'] not in L:
            L.append(G.nodes[i]['currency'])
    return len(L)


#Test des fonctions pour le cas de deux communautés


pintra=0.3
pinter=0.05
B=nx.Graph() 
B.add_nodes_from(range(1,N+1)) 

for i in range(1,N+1):
    B.nodes[i]['currency']=str(i)

for i in range(1,(N//2)+1):
    for j in range(i+1,(N//2)+1):
        if random.random()<pintra:
            B.add_edge(i, j)
    for j in range((N//2)+1,N+1):
        if random.random()<pinter:
            B.add_edge(i,j)
for i in range((N//2)+1,N+1):
    for j in range(i+1,N+1):
        if random.random()<pintra:
            B.add_edge(i,j)

print("B:",B)
print("L'utilité sociale de B est",social_utility_hetero(B))
print("Le nombre de devises dans B est",currencies_number(B))

L=set(B.nodes[i]['currency'] for i in B.nodes())

print("Les devises dans le système final sont:",L)



#La fonction qui retourne la moyenne sur 10000 systèmes des nombres de devises à l'état final


def mean_currencies(pintra,pinter, n):
    '''Cette fonction ajoute à chaque étape le nombre de devises 
    à l'état final d'un graphe aléatoire avec une probabilité pinter
    de connexion entre deux noeuds de la même communauté, et 
    une probabilité pintra de connexion entre deux noeuds
    de communautés différentes, puis divise par le nombre 
    de graphes considérés (10000 dans ce cas) afin d'avoir une 
    moyenne.

    Args:
        p(float): Probabilité de connection entre deux noeuds
        n(int) : Nombre de systèmes étudiés
    
    Returns:
        La moyenne des nombres de devises à l'état final
    '''

    s=0
    for i in range(n):

        G=nx.Graph() 

        G.add_nodes_from(range(1,N+1)) 

        for i in range(1,N+1):
            G.nodes[i]['currency']=str(i)

          
        for i in range(1,(N//2)+1):
            for j in range(i+1,(N//2)+1):
                if random.random()<pintra:
                    G.add_edge(i, j)
            for j in range((N//2)+1,N+1):
                if random.random()<pinter:
                    G.add_edge(i,j)
        for i in range((N//2)+1,N+1):
            for j in range(i+1,N+1):
                if random.random()<pintra:
                    G.add_edge(i,j)

        s+=currencies_number(G)

    return(s/n)



#Tests de cette fonction

print("La moyenne pour pintra=0.3 et pinter=0.01 sur 10 systèmes est égale à",mean_currencies(0.3,0.01,10))
print("La moyenne pour pintra=0.3 et pinter=0.01 sur 100 systèmes est égale à",mean_currencies(0.3,0.01,100))
print("La moyenne pour pintra=0.3 et pinter=0.05 sur 10 systèmes est égale à",mean_currencies(0.3,0.05, 10))
print("La moyenne pour pintra=0.3 et pinter=0.2 sur 10 systèmes est égale à",mean_currencies(0.3,0.2, 10))






#On trace les résultats pour plusieurs valeurs de pintra et pour pinter=0.3

P=np.linspace(0,0.3,10)
n=10
M=[]
for pinter in P:
    M.append(mean_currencies(0.3,pinter, n))

plt.plot(P,M)
plt.xlabel("pinter, probabilité d'échanger avec les voisins de l'autre communauté")
plt.ylabel("Nombre de devises à l'équilibre")
plt.title("Moyenne du nombre de devises à l équilibre selon différentes valeurs de pinter pour pintra=0.3 avec des agents hétérogènes")
plt.show() 

######Deuxième cas: chaque communauté a sa propre devise######


'''On reprend les fonctions précédentes, et on modifie 
seulement la manière de construire le graphe, de telle 
sorte à ce qu'il y ait deux communautés ayant chacune au départ une monnaie unique. 
Il y a donc à l'état initial 2 monnaies dans le graphe.'''



pintra=0.3
pinter=0.05
B2=nx.Graph() 
B2.add_nodes_from(range(1,N+1)) 

for i in range(1,(N//2)+1):
    B2.nodes[i]['currency']=1
for i in range((N//2)+1,N+1):
    B2.nodes[i]['currency']=2

for i in range(1,(N//2)+1):
    for j in range(i+1,(N//2)+1):
        if random.random()<pintra:
            B2.add_edge(i, j)
    for j in range((N//2)+1,N+1):
        if random.random()<pinter:
            B2.add_edge(i,j)
for i in range((N//2)+1,N+1):
    for j in range(i+1,N+1):
        if random.random()<pintra:
            B2.add_edge(i,j)

print("B2:",B2)
print("L'utilité sociale de B2 est",social_utility_hetero(B))
print("Le nombre de devises dans B2 est",currencies_number(B))

L2=set(B2.nodes[i]['currency'] for i in B2.nodes())

print("Les devises dans le système final lorsque les communautés ont chacune une devise unique à l'état intial sont:",L2)
#On trace les résultats pour plusieurs valeurs de pintra et pour pinter=0.3

P=np.linspace(0,0.3,10)
n=10
M=[]
for pinter in P:
    M.append(mean_currencies(0.3,pinter, n))

plt.plot(P,M)
plt.xlabel("pinter, probabilité d'échanger avec les voisins de l'autre communauté")
plt.ylabel("Nombre de devises à l'équilibre")
plt.title("Agents hétérogènes : Moyenne du nombre de devises à l équilibre selon différentes valeurs de pinter pour pintra=0.3, lorsqu'il n'y a que deux devises au départ")
plt.show() #attention à la valeur de n, si n trop grand, le programme est long à s'exécuter

'''Conclusion : On obtient les mêmes conclusions que lorsque les agents n'étaient pas hétérogènes. 
L'hétérogénéité n'a un impact que sur le choix de la ou des monnaies dominantes. Mais pas sur le nombre de devise à l'équilibre.'''
