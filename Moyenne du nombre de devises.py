


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


    


