
#On commence par déterminer quelle devise est la plus utilisée par les voisins de i, ensuite on modifie la devise de i.
#Si plusieurs devises sont utilisées par le même nombre maximal de voisins, on choisit aléatoirement l'une de ces devises.

def change_currency(i,G):
    neighbors=list(G.neighbors(i))
    d={}
    for j in neighbors:
        if G.nodes[j]['currency'] not in d:
            d[G.nodes[j]['currency']]=1
        else:
            d[G.nodes[j]['currency']]+=1
    max=max(d.values())
    L=[j for j,v in d.items() if v==max]
    G.nodes[i]['currency']=random.choice(L)

