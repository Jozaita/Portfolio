import numpy as np 
import networkx as nx
import random as rd
import time
from matplotlib import pyplot as plb
start=time.time()
#Condiciones de la poblacion
N=40
tfinal=5000
def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]
fraccop=[i for i in range(0,tfinal)]
agents=[i for i in range(0,N)]
satisf=[]
atributos=[0*N]
a=np.array([1,0])
b=np.array([0,1])
#a=a.reshape(2,1)
#b=b.reshape(2,1)
states=[a,b]
A=np.zeros([2,2])
A[0,0]=r=1
A[1,0]=s=0
A[0,1]=t1=1
A[1,1]=p=0
#Definimos la grafica y ponemos el estado inicial 
G=nx.fast_gnp_random_graph(N,0.7)
for i in range(0,N):
    G.node[i]['v']=rd.choice(states)
values=[G.nodes(data='v')[i][0] for i in  range(0,N)] 
fraccop[0]=sum(values)/N  
 #A cada paso, escogemos un nodo que juega a PD con sus vecinos
 
for t in range(1,tfinal) :
    print(t)
    satisf=[]
    payoff=np.zeros([N])  
    for part in agents:       
        for i in list(G.neighbors(part)):
            
            u=nx.get_node_attributes(G,'v')[part]
            u2=nx.get_node_attributes(G,'v')[i]
            for k in range(0,len(u)):
                for k2 in range(0,len(u2)):
                    payoff[part]=payoff[part]+u[k]*A[k2,k]*u2[k2]
                 
#Una vez jugado una ronda, se cambia la estrategia
    for j in agents:
        payme=payoff[i]
        vecinos=list(G.neighbors(j))
        payrest=[payoff[i] for i in vecinos]
        agents1=agents
        paywin=max(payrest)
        if payme<paywin:
            satisf.append(j)
            k=payrest.index(paywin)
            k=vecinos[k]
            if values[k]==0 and values[j]==0 and j in satisf:
                  p=rd.uniform(0,1)
                  q=0
                  if p<q: 
                      k11=diff(agents,vecinos)
                      k1=rd.choice(diff(k11,[j]))
                      while (G.has_edge(j,k1))==True:
                          k1=rd.choice(diff(k11,[j]))
                      #print(j,vecinos2,k1)
                      G.add_edge(j,k1)
                      G.remove_edge(j,k)
                      
            else:        
                  G.node[j]['v']=nx.get_node_attributes(G,'v')[k]
                  values[j]=G.nodes(data='v')[i][0]
#Acorde al paper cambiamos la estrategia de uno aleatoriamente, para evitar
# estados congelados            
    j=rd.choice(range(0,N))
    G.node[j]['v']=rd.choice(states)
    values=[G.nodes(data='v')[i][0] for i in  range(0,N)] 
    fraccop[t]=sum(values)/N
#Hay que tomar medidas a cada tiempo 

#Ploteamos la network            
#f2=plb.figure()
#nx.draw(G,node_color=values)
f1=plb.figure()
plb.plot(fraccop)

tiempo=time.time()-start
print(tiempo)    