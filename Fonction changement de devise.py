
#On commence par déterminer quelle devise est la plus utilisée par les voisins de i, ensuite on modifie la devise de i.
#Si plusieurs devises sont utilisées par le même nombre maximal de voisins, on choisit aléatoirement l'une de ces devises (en laissant la priorité à la devise utilisée par i).

def change_currency(i,G):
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



