import random
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import Counter

'''On reprend les mêmes simulations que précédemment mais en ajoutant l'impact d'agents hétérogènes'''


''' Cette méthode choisit les agents dans l'ordre et ne permet pas
de changer leurs devises simultanément ''' 


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


    neighbors=list(G.neighbors(i)) #création liste des voisins de l'agent i
    if neighbors:
        d=Counter([G.nodes[j]['currency'] for j in neighbors]) #renvoie les devises dans un dictionnaire d avec leurs occurences
        currency_max=max(d,key=d.get)#trouve la devise avec le plus d'occurence
        if G.nodes[i]['currency']!=currency_max:
            count_max=max(d.values())#donne le nombre max d'occurences
            currencies_max=[j for j,s in d.items() if s==count_max]#liste des devises ayant le nombre max d'occurence 
            if G.nodes[i]['currency'] in currencies_max: #si la devise de i fait partie des devises avec le plus d'occurence, i garde sa devise par défaut
                currency=G.nodes[i]['currency']
            else:
                currency=random.choice(currencies_max) #sinon il en prend une au hasard
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


#Tracé de l'évolution de l'utilité sociale 

p=0.8
C=nx.Graph() 
C.add_nodes_from(range(1,N+1)) 

#initialisation du graphe, chaque agent i possède sa devise s(i)=i au départ
for i in range(1,N+1):
    C.nodes[i]['currency']=str(i)

#avec une probabilité p, l'agent i échange avec son voisin,si c'est le cas on ajoute une arrête entre les deux noeuds modélisant le lien entre les agents i et j
for i in range(1,N+1):
    for j in range(i+1,N+1):
        if random.random()<p:
            C.add_edge(i, j)

#calcul de l'utilité sociale
U=[social_utility_hetero(C)]
u=social_utility_hetero(C)
precedent=None
while u!=precedent:
    precedent=u
    for i in C.nodes():
        change_currency(i,C)
        u=social_utility_hetero(C)
        U.append(u)
X=[i for i in range(len(U))]
print(U)
plt.plot(X,U)
plt.xlabel("temps")
plt.ylabel("Utilité sociale")
plt.title("Evolution de l'utilité sociale dans le temps avec des agents hétérogènes")
plt.show()



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
#on cherche un équilibre pour compter le nombre de dévises à l'équilibre
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
print("L'utilité sociale de B est",social_utility_hetero(B))
print("Le nombre de devises dans B est",currencies_number(B))

L=set(B.nodes[i]['currency'] for i in B.nodes())

print("Les devises dans le système final sont:",L)




#La fonction qui retourne la moyenne sur n systèmes des nombres de devises à l'état final

def mean_currencies(p,n):
    '''Cette fonction ajoute à chaque étape le nombre de devises 
    à l'état final d'un graphe aléatoire avec une probabilité p
    de connexion entre deux noeuds, puis divise par le nombre 
    de graphes considérés (10000 dans ce cas) afin d'avoir une 
    moyenne.

    Args:
        p(float): Probabilité de connexion entre deux noeuds
        n(int): nombre de systèmes
    
    Returns:
        La moyenne des nombres de devises à l'état final
    '''

    s=0
    for i in range(n):

        G=nx.Graph() 

        G.add_nodes_from(range(1,N+1)) 

        for i in range(1,N+1):
            G.nodes[i]['currency']=str(i)

        for i in range(1,N+1):
            for j in range(i+1,N+1):
                if random.random()<p:
                    G.add_edge(i, j)

        s+=currencies_number(G)

    return(s/n)





#Tests de cette fonction

'''
print("La moyenne pour p=0.1 sur 10 systèmes est égale à",mean_currencies(0.1, 10))
print("La moyenne pour p=0.1 sur 1000 systèmes est égale à",mean_currencies(0.1, 1000))
print("La moyenne pour p=0.05 sur 100 systèmes est égale à",mean_currencies(0.05, 100))
print("La moyenne pour p=0.05 sur 1000 systèmes est égale à",mean_currencies(0.05, 1000))
print("La moyenne pour p=0.8 sur 100 systèmes est égale à",mean_currencies(0.8, 100))
print("La moyenne pour p=0.8 sur 1000 systèmes est égale à",mean_currencies(0.8, 1000))
print("La moyenne pour p=0.001 sur 1000 systèmes est égale à",mean_currencies(0.1, 1000))'''



''' On remarque que pour p>0.1, cette moyenne est égale à 1. 
Intuitivement, plus les agents sont connectés, plus ils sont
amenés à avoir une seule devise commune. De façon analogue, lorsque 
p tend vers 0, la moyenne tend vers 100'''





#On trace les résultats pour plusieurs valeurs de p pour 100 systèmes

n=10
P=np.linspace(0,1,100)
M=[]
for p in P:
    M.append(mean_currencies(p, n))

plt.plot(P,M)
plt.xlabel("p, probabilité d'échanger avec ses voisins")
plt.ylabel("Nombre de devises à l'équilibre")
plt.title("Moyenne du nombre de devises à l équilibre selon différentes valeurs de p avec des agents hétérogènes")
plt.show() #Complexité élevée, prend trop de tps à être executé

'''Plus p tend vers 0, plus la moyenne tend vers 100.
Inversement, plus p tend vers 1, plus la moyenne tend vers 1'''


'''Conclusion : On obtient les mêmes conclusions que lorsque les agents n'étaient pas hétérogènes. 
L'hétérogénéité n'a un impact que sur le choix de la ou des monnaies dominantes. Mais pas sur le nombre de devise à l'équilibre.'''
