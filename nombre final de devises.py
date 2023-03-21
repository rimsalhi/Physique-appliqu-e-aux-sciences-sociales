import random
import matplotlib.pyplot as plt
import networkx as nx

N=100


def social_utility(G):
    u=0
    for i in G.nodes():
        for j in G.neighbors(i):
            if G.nodes[i]['currency']!=G.nodes[j]['currency']:
                u+=-0.5
    return u


#Étant donné une probabilité p, on calcule le nombre de devises distinctes dans le système final 

def currencies_number(G):
    u=social_utility(G)
    precedent=None
    while True:
        precedent=u
        for i in G.nodes():
            change_currency(i,G)
        u=social_utility(G)
        assert u!=precedent
    L=[]
    for i in G.nodes:
        if G.nodes[i]['currency'] not in L:
            L.append(G.nodes[i]['currency'])
    return len(L)
        
