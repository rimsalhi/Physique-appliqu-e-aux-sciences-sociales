import numpy as np
N=100
p=0.05

def mean_currencies(p):
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


print(mean_currencies(0.1))
print(mean_currencies(0.05))
print(mean_currencies(0.5))
print(mean_currencies(0.8))

P=np.linspace(0,1,10)
M=[]
for p in P:
    M.append(mean_currencies(p))

plt.plot(P,M)
plt.show() #Complexité élevée, prend trop de tps à être executé


    


