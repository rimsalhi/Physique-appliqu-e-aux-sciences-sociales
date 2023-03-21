
#On commence par déterminer quelle devise est la plus utilisée par les voisins de i, ensuite on modifie la devise de i.

def change_currency(i,G):
    neighbors=list(G.neighbors(i))
    d={}
    for j in neighbors:
        if G.nodes[j]['currency'] not in d:
            d[G.nodes[j]['currency']]=1
        else:
            d[G.nodes[j]['currency']]+=1
    max=max(d.items()[0], key=lambda x: x[1])
    G.nodes[i]['currency']=max

