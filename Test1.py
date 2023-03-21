# Test de la fonction currencies_number

N=100
p=0.05
B=nx.Graph() 
B.add_nodes_from(range(1,N+1)) 

for i in range(1,N+1):
    B.nodes[i]['currency']=str(i)

for i in range(1,N+1):
    for j in range(i+1,N+1):
        if random.random()<p:
            B.add_edge(i, j)
    

u=social_utility(B)
precedent=None
while u!=precedent:
    precedent=u
    for i in B.nodes():
        change_currency(i,B)
    u=social_utility(B)

print(u)

L=[]
for i in B.nodes:
    if B.nodes[i]['currency'] not in L:
        L.append(B.nodes[i]['currency'])
    

print(L)
    
print(B)
print(social_utility(B))
print(currencies_number(B))