import numpy as np 
import networkx as nx
import random as rd
import time
from matplotlib import pyplot as plb
#Condiciones de la poblacion
N=10
tfinal=1000
sim=2
trange=np.arange(1,2,0.05)
mediacop=[0]*(len(trange))
varianzacop=[0]*(len(trange))
mediadeg=[0]*(len(trange))
varianzadeg=[0]*(len(trange))
fraccop=[0]*tfinal
fraccop2=[0]*tfinal
varcop=[0]*tfinal
averdeg=[0]*tfinal
vardeg=[0]*tfinal
start=time.time()
#Condiciones de la estadistica
for t1 in trange:
  print(t1)
  for s in range(0,sim): 
   print(s,time.time()-start)

  
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
   A[0,1]=t1
   A[1,1]=p=0
#Definimos la grafica y ponemos el estado inicial 
   G=nx.fast_gnp_random_graph(N,0.7)
   for i in range(0,N):
      G.node[i]['v']=rd.choice(states)
   values=[G.nodes(data='v')[i][0] for i in  range(0,N)] 
   fraccop[0]=fraccop[0]+sum(values)/N
   fraccop2[0]=fraccop[0]+(sum(values)/N)**2
   averdeg[0]=averdeg[0]+G.degree(i)/N
   vardeg[0]=vardeg[0]+(G.degree(i)**2/N)
 #A cada paso, escogemos un nodo que juega a PD con sus vecinos
 
   for t in range(1,tfinal) :
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
              G.node[j]['v']=nx.get_node_attributes(G,'v')[k]
#Rewire con probabilidad p los enlaces de menor beneficiok
              if values[k]!=1 and values[j]!=1 and i!=k:
                  p=rd.uniform(0,1)
                  if p>0.01:
                      G.remove_edge(j,k)
                      agents1=agents.remove(j)
                      G.add_edge(j,agents1)
#Acorde al paper cambiamos la estrategia de uno aleatoriamente, para evitar
# estados congelados            
      j=rd.choice(range(0,N))
      G.node[j]['v']=rd.choice(states)
      values=[G.nodes(data='v')[i][0] for i in  range(0,N)] 
      fraccop[t]=fraccop[t]+sum(values)/N
      fraccop2[t]=fraccop[t]+(sum(values)/N)**2
      averdeg[t]=averdeg[t]+sum([G.degree(i)/N for i in range(0,N)])
      vardeg[t]=vardeg[t]+sum([(G.degree(i)**2/N) for i in range(0,N)])
#Hay que tomar medidas a cada tiempo 
  for i in range(0,len(fraccop)):
    fraccop[i]=fraccop[i]/sim
    varcop[i]=fraccop2[i]/sim-fraccop[i]**2
    averdeg[i]=averdeg[i]/sim
    vardeg[i]=vardeg[i]/sim-averdeg[i]**2
  mediacop[int(t1/trange[1])]=np.average(fraccop[:int(tfinal/2)])
  varianzacop[int(t1/trange[1])]=np.average(varcop[:int(tfinal/2)])
  mediadeg[int(t1/trange[1])]=np.average(averdeg[:int(tfinal/2)])
  varianzadeg[int(t1/trange[1])]=np.average(vardeg[:int(tfinal/2)])  
  
  tiempo=time.time()-start
print(tiempo)
#f1=plb.figure()
#plb.plot(fraccop)
#plb.plot(varcop)
#f3=plb.figure()
#plb.plot(averdeg)
#plb.plot(vardeg)


    