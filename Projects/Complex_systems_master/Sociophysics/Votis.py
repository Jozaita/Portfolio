import numpy as np 
import networkx as nx
import random as rd
import time
import sys
from matplotlib import pyplot as plb
N=100
tfinal=N*10**2
mag=[0]*tfinal
pob=[0]*tfinal
ag=[i for i in range(0,N)]
G=nx.Graph()
G.add_nodes_from([i for i in range(0,N)])
for i in range(0,int(8*N)):
       i1=rd.choice(ag)
       i2=rd.choice(ag)
       while G.has_edge(i1,i2)==True:
         i2=rd.choice(ag)
       G.add_edge(i1,i2)

for k in range(0,N):
    G.node[k]['m']=rd.choice([-1,1])

med=[G.nodes(data='m')[i] for i in  range(0,N)] 




for i in range(0,tfinal):
    j=rd.choice(ag)
    
    
    vec=list(G.neighbors(j))
    tar=rd.choice(vec)
    G.node[j]['m']=G.node[tar]['m']
    med=[G.nodes(data='m')[i] for i in  range(0,N)]
        
    
        #G.remove_edge(j,tar)
        #G.add_edge(j,rd.choice(ag))
    
    
    for o in range(0,len(ag)):
        
        pob[i]=sum(med)
    pob[i]=pob[i]/N
plb.plot(pob)