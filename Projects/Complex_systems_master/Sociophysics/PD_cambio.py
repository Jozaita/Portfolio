import numpy as np 
import networkx as nx
import random as rd
import time
import sys
from matplotlib import pyplot as plb
#Condiciones de la poblacion
def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]
N=100
tfinal=50
sim=100
trange=np.arange(1,2,0.05)
mediacop=[0]*(len(trange))
varianzacop=[0]*(len(trange))
mediadeg=[0]*(len(trange))
varianzadeg=[0]*(len(trange))
varianzanorm=[0]*(len(trange))
varianzanorm1=[0]*(len(trange))
fraccop=[0]*tfinal
fraccop2=[0]*tfinal
varcop=[0]*tfinal
averdeg=[0]*tfinal
probdef=[0]*tfinal
probcop=[0]*tfinal
vardeg=[0]*tfinal
agents=[i for i in range(0,N)]
satisf=[]
a=np.array([1,0])
b=np.array([0,1])

mediacop=[0]*(len(trange))
varianzacop=[0]*(len(trange))

mediadeg=[0]*(len(trange))
varianzadeg=[0]*(len(trange))
states=[a,b]
start=time.time()
#Condiciones de la estadistica
for t1 in trange:
  conta=0
  indice=0
  for s in range(0,sim):
   
   payoffvec=[0]*tfinal      
   fraccop=[0]*tfinal
   fraccop2=[0]*tfinal  
   varcop=[0]*tfinal
   averdeg=[0]*tfinal
   vardeg=[0]*tfinal   
   print(t1,s,mediacop[indice])
   indice=int((t1-trange[0])/(trange[1]-trange[0]))
   A=np.zeros([2,2])
   A[0,0]=r=1
   A[1,0]=s=0
   A[0,1]=t1
   A[1,1]=p=0
   #Definimos la grafica y ponemos el estado inicial 
   G=nx.Graph()
   G.add_nodes_from([i for i in range(0,N)])
   for i in range(0,int(2.5*N)):
       i1=rd.choice(agents)
       i2=rd.choice(agents)
       while G.has_edge(i1,i2)==True:
         i2=rd.choice(agents)
       G.add_edge(i1,i2)
   #G=nx.random_degree_sequence_graph([4]*N)
   #G=nx.random_regular_graph(4,N)
   pos=nx.spring_layout(G)
   inicond=[a]*int(0.6*N)+[b]*int(0.4*N)
   rd.shuffle(inicond)
   for i in range(0,N):
      G.node[i]['v']=inicond[i]
     
   values=[G.nodes(data='v')[i][0] for i in  range(0,N)] 
   fraccop[0]=fraccop[0]+sum([values[i] for i in range(0,N)])/N
   averdeg[0]=averdeg[0]+sum([G.degree(i) for i in range(0,N)])/N
   vardeg[0]=vardeg[0]+sum([(G.degree(i)**2) for i in range(0,N)])/N
 #A cada paso, escogemos un nodo que juega a PD con sus vecinos
   
   
   for t in range(1,tfinal):
      
      unsatisf=[]
      payoff=np.zeros([N])  
      for part in agents:       
          for i in list(G.neighbors(part)):
              u=nx.get_node_attributes(G,'v')[part]
              u2=nx.get_node_attributes(G,'v')[i]
              for k in range(0,len(u)):
                  for k2 in range(0,len(u2)):
                      payoff[part]=payoff[part]+u[k]*A[k2,k]*u2[k2]
      payoffvec[t]=sum(payoff)/N       
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
              G.node[j]['v']=nx.get_node_attributes(G,'v')[k]
              values[j]=G.nodes(data='v')[j][0]
             
#Rewire con probabilidad p los enlaces de menor beneficio
      #if t>50:
      for j in unsatisf:
          vecinos=list(G.neighbors(j))
          for k in vecinos:
              if values[k]==0 and values[j]==0 :
                  p=rd.uniform(0,1)
                  q=0
                  if p>q:
                      #vecinos2=list(G.neighbors(j))
                      k11=diff(agents,vecinos)
                      k1=rd.choice(diff(k11,[j]))
                      #print(j,vecinos2,k1)
                      #k1=rd.choice(agents)
                      #while G.has_edge(j,k1)==True:
                      #    k1=rd.choice(agents)
                      G.add_edge(j,k1)
                      G.remove_edge(j,k)
#Acorde al paper cambiamos la estrategia de uno aleatoriamente, para evitar
# estados congelados
      #links=list(G.edges())
      
      #for ih in links: 
       #   if values[ih[0]]==0 and values[ih[1]]==0:
       #       probdef[t]=probdef[t]+1/len(links)
       #   if values[ih[0]]==1 and values[ih[1]]==1:
       #       probcop[t]=probcop[t]+1/len(links)
                   
      #j=rd.choice(range(0,N))
      #G.node[j]['v']=rd.choice(states)
      values=[G.nodes(data='v')[i][0] for i in  range(0,N)] 
      fraccop[t]=fraccop[t]+sum([values[i] for i in range(0,N)])/N
      averdeg[t]=averdeg[t]+sum([G.degree(i) for i in range(0,N)])/N
      vardeg[t]=vardeg[t]+sum([(G.degree(i)**2) for i in range(0,N)])/N
    
   
   if fraccop[tfinal-1]>0.05:   
    mediacop[indice]+=np.average(fraccop[:int(tfinal/2)])
    varianzacop[indice]+=np.var(fraccop[:int(tfinal/2)])
    mediadeg[indice]+=np.average(averdeg[:int(tfinal/2)])
    varianzadeg[indice]+=np.average(vardeg[:int(tfinal/2)])
    conta=conta+1       
   #print(t1,s,mediacop[indice]) 
   
#Hay que tomar medidas a cada tiempo 
  tiempo=time.time()-start
  print(tiempo)
  if conta!=0:
   mediacop[indice]=mediacop[indice]/conta
   varianzacop[indice]=varianzacop[indice]/conta
   mediadeg[indice]=mediadeg[indice]/conta
   varianzadeg[indice]=varianzadeg[indice]/conta 
   varianzanorm1[indice]=(varianzacop[indice]-mediacop[indice]**2)/mediacop[indice]
   varianzanorm[indice]=(varianzadeg[indice]-mediadeg[indice]**2)/mediadeg[indice]
   
  
plb.plot(trange,mediacop)
#f1=plb.figure()
#plb.plot(fraccop)
#plb.plot(varcop)
#f3=plb.figure()
#plb.plot(averdeg)
#plb.plot(vardeg)


    