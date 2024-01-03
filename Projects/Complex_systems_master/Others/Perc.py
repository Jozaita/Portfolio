import numpy as np 
import networkx as nx
import random as rd
import time
import sys
from matplotlib import pyplot as plb
#Condiciones de la poblacion
N=10**3
t=1
tfinal=10**4

h=2.33
a=1/(h+1)

states=[-1,1]
size=[0]*tfinal
ci=[0]*tfinal
ret=[0]*tfinal
#rnorm=[0]*tfinal
pre=[0]*tfinal
pre[0]=100
lambda1=5*10**4
start=time.time()
 #Definimos la grafica y ponemos el estado inicial 
G=nx.Graph()
G.add_nodes_from([i for i in range(0,N)])
for i in range(0,N):
     G.node[i]['v']=0
values=[G.nodes(data='v')[i] for i in  range(0,N)] 

def destroy(j):
    drl=[j]
    while drl!=[]:
     for ij in drl: 
        desnei=list(G.neighbors(ij))
        if desnei!=[]:
         for ik in desnei:
           G.nodes[ik]['v']= G.nodes[ij]['v']
           G.remove_edge(ik,ij)
     drl=[]
     if desnei!=[]:
      for il in range(0,len(desnei)):
        drl.append(desnei[il])
    return

  #Introduce the dynamics for each timestep 
while t<tfinal:

      
      for i in range(0,N):
          G.node[i]['v']=0
          
      j=rd.randint(0,N-1)
      u=rd.uniform(0,1)
      #if t==3 :
       # sys.exit()
      
      
      if u<a:
           G.node[j]['v']=rd.choice(states)
           #destroy(j)
           G2=list(nx.connected_component_subgraphs(G))
           
           lenG2=len(G2)
           for k in range(0,lenG2):
               if j in list(G2[k].nodes()):
                   G2b=G2[k]
                   
           for ik in list(G2b.nodes()):
               G.node[ik]['v']=G.node[j]['v']
                    
               

   #Calculate s 
           values=[G.nodes(data='v')[i] for i in  range(0,N)] 
           si=sum(values)
           ci[t]=len(G.edges())/N
           size[t]=abs(si)
           pre[t]=pre[t-1]*np.exp(si/lambda1)
           r=pre[t]/pre[t-1]
           ret[t]=np.log(r)
      
           linksd=list(G2b.edges())
           for l in  range(0,len(linksd)):
                    G.remove_edge(linksd[l][0],linksd[l][1])
           t=t+1
           if np.mod(t*100,tfinal)==0:
            print(time.time()-start)
           
      else:
        k=rd.randint(0,N-1)
        while k==j and G.has_edge(k,j):
            k=rd.randint(0,N-1)
        G.add_edge(k,j)
               
          

hist1=np.histogram(size,bins=100,range=(1,max(size)),normed=1)
f1=plb.figure()
ax=plb.gca()
plb.loglog(hist1[1][:-1],hist1[0],'o')
hist2=np.histogram(ret,bins=100,normed=1)
f2=plb.figure()
ax=plb.gca()
plb.loglog(hist2[1][:-1],hist2[0],'o')
#hist3=np.histogram(rnorm,bins='fd',range=(1,max(rnorm)),normed=1)
#f1=plb.figure()
#ax=plb.gca()
#plb.loglog(hist1[1][:-1],hist1[0],'o')
print(time.time()-start)            
f2.savefig('Return.eps')
f1.savefig('Sizecluster.eps')