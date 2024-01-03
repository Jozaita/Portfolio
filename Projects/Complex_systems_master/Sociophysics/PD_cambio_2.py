import numpy as np 
import networkx as nx
import random as rd
import time
import sys
import csv
from matplotlib import pyplot as plb
#Condiciones de la poblacion
def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]
N=300
tfinal=1000
sim=1
trange=[1.5]
mediacop=[0]*(len(trange))
varianzacop=[0]*(len(trange))
mediadeg=[0]*(len(trange))
varianzadeg=[0]*(len(trange))
varianzanorm=[0]*(len(trange))
fraccop=[0]*tfinal
fraccop2=[0]*tfinal
varcop=[0]*tfinal
averdeg=[0]*tfinal
vardeg=[0]*tfinal
agents=[i for i in range(0,N)]
satisf=[]
a=np.array([1,0])
b=np.array([0,1])
probdef=[0]*tfinal
mediacop=[0]*(len(trange))
varianzacop=[0]*(len(trange))
mediadeg=[0]*(len(trange))
varianzadeg=[0]*(len(trange))
states=[a,b]
start=time.time()
#Condiciones de la estadistica
for t1 in trange:
  print(t1,time.time()-start)
  for s in range(0,sim): 
   
   fraccop=[0]*tfinal
   fraccop2=[0]*tfinal  
   varcop=[0]*tfinal
   averdeg=[0]*tfinal
   vardeg=[0]*tfinal
   A=np.zeros([2,2])
   A[0,0]=r=1
   A[1,0]=s=0
   A[0,1]=t1
   A[1,1]=p1=0
   #Definimos la grafica y ponemos el estado inicial 
   G=nx.random_degree_sequence_graph([4]*N)
   pos=nx.spring_layout(G)
   inicond=[a]*int(0.6*N)+[b]*int(0.4*N)
   rd.shuffle(inicond)
   for i in range(0,N):
      G.node[i]['v']=inicond[i]
      
   values=[G.nodes(data='v')[i][0] for i in  range(0,N)] 
   fraccop[0]=fraccop[0]+sum(values)/N
   fraccop2[0]=fraccop[0]+(sum(values)/N)**2
   averdeg[0]=averdeg[0]+G.degree(i)/N
   vardeg[0]=vardeg[0]+(G.degree(i)**2/N)
 #A cada paso, escogemos un nodo que juega a PD con sus vecinos
 
   for t in range(1,tfinal) :
      unsatisf=[]
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
          payme=payoff[j]
          vecinos=list(G.neighbors(j))
          if vecinos!=[]:
           payrest=[payoff[i] for i in vecinos]
           paywin=max(payrest)
           if payme<paywin:
              unsatisf.append(j)
              k=payrest.index(paywin)
              k=vecinos[k]
              #Rewire con probabilidad q los enlaces de menor beneficio
              if values[k]==0 and values[j]==0 and j in unsatisf:
                  p=rd.uniform(0,1)
                  q=0.01
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
      links=list(G.edges())
      lenlinks=len(links)
      for ih in links: 
          if values[ih[0]]==0 and values[ih[1]]==0:
              probdef[t]=probdef[t]+1/lenlinks                
      
      values=[G.nodes(data='v')[i][0] for i in  range(0,N)] 
      fraccop[t]=fraccop[t]+sum(values)/N
      fraccop2[t]=fraccop[t]+(sum(values)/N)**2
      averdeg[t]=averdeg[t]+sum([G.degree(i)/N for i in range(0,N)])
      vardeg[t]=vardeg[t]+sum([(G.degree(i)**2/N) for i in range(0,N)])
      varcop[t]=fraccop2[t]-fraccop[t]**2
      vardeg[t]=vardeg[t]-averdeg[t]**2
      print(t,fraccop[t],probdef[t])
      j=rd.choice(range(0,N))
      G.node[j]['v']=rd.choice(states)
#Hay que tomar medidas a cada tiempo 
  
  indice=int((t1-trange[0])/(trange[1]-trange[0]))
  mediacop[indice]=np.average(fraccop[:int(tfinal/2)])
  varianzacop[indice]=np.average(varcop[:int(tfinal/2)])
  mediadeg[indice]=np.average(averdeg[:int(tfinal/2)])
  varianzadeg[indice]=np.average(vardeg[:int(tfinal/2)])  
  varianzanorm[indice]=varianzadeg[indice]/mediadeg[indice]
  tiempo=time.time()-start
print(tiempo)
#f1=plb.figure()
#plb.plot(fraccop)
#plb.plot(varcop)
#f3=plb.figure()
#plb.plot(averdeg)
#plb.plot(vardeg)


    