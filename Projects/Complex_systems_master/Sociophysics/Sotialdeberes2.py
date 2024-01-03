import numpy as np 
import networkx as nx
import random as rd
import time
import sys
from matplotlib import pyplot as plb

start=time.time()
#Global parameters of the problem 
L=4
N=L**2
tfin=N*10**4
F=10
q=10
qmin=2
qmax=100
qvec=np.arange(qmin,qmax)
smax=[0]*(qmax-qmin)
indice=0

for q in qvec:
#Local parameters (for an event)
    colores=np.zeros([L,L])

#Lattice implementation 
    G=nx.grid_graph(dim=[L,L],periodic=True)

#Choose initial  attributes for each node(uni not poiss) 

    for i in range(0,L):
        for j in range(0,L):
            #a ver si así ahorramos tiempo 
            p=i*L+j
            for k in range(1,F+1):
                G.node[i,j][str(k)]=rd.choice([i for i in range(1,q)])
    
#Begin the dynamics 
    t=0            
    while t<tfin:
        i1=rd.randint(0,L-1)
        i2=rd.randint(0,L-1)
        vec=list(G.neighbors((i1,i2)))
        obj=rd.choice(vec)
        feat=rd.randint(1,F)
        if G.node[i1,i2][str(feat)]==G.node[obj[0],obj[1]][str(feat)]:
            feat2=rd.randint(1,F)
            while feat2==feat:
                feat2=rd.randint(1,F)
            G.node[i1,i2][str(feat2)]=G.node[obj[0],obj[1]][str(feat2)]
            t=t+1
    #Choose attribute to compare 
    for k in range(1,F+1):
        for p1 in range(0,L):
            for p2 in range(0,L):
                colores[p1,p2]=colores[p1,p2]+G.node[p1,p2][str(k)]*10**(k)
    #plb.imshow(colores)


    nodos=list(G.nodes())
    G2=nx.Graph()
    G2.add_nodes_from(nodos)
    for s1 in range(0,L):
        for s2 in range(0,L):
            for o1 in range(0,L):
                for o2 in range(0,L):
                    if colores[s1,s2]==colores[o1,o2]:
                        G2.add_edge((s1,s2),(o1,o2))
    giant=max(nx.connected_component_subgraphs(G2),key=len)
    
    smax[indice]=len(giant)/N
    indice=indice+1
    print(q,smax[indice])



finish=time.time() 
print(finish-start)       