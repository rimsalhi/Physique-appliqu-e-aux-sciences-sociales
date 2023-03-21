# Test de la fonction currencies_number

N=100
p=0.5
B=nx.Graph() 
B.add_nodes_from(range(1,N+1)) 

for i in range(1,N+1):
    B.nodes[i]['currency']='i'

for i in range(1,N+1):
    for j in range(i+1,N+1):
        if random.random()<p:
            B.add_edge(i, j)
    

print(social_utility(B))
print(currencies_number(B))