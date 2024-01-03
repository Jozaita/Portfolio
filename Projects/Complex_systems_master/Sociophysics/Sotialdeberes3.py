import numpy as np 
import networkx as nx
import random as rd
import time

import sys
from matplotlib import pyplot as plb

start=time.time()
#Global parameters of the problem 
L=10
N=L**2
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
    G=nx.grid_graph(dim=[L,L],periodic=False)

#Choose initial  attributes for each node(uni not poiss) 

    for i3 in range(0,L*(L)):
            j=int(np.mod(i3,L))
            i=int((i3-j)/L)
            
            #a ver si así ahorramos tiempo 
            for k in range(0,F):
                G.node[i,j][(k)]=rd.choice([i for i in range(1,q)])
                
    edges=list(G.edges())
    lenedges=len(G.edges())
    actlinks=[0]*lenedges
    for y1 in range(0,lenedges):
                edgep=edges[y1]
                atrs=list(G.node[edgep[0][0],edgep[0][1]].values())
                atro=list(G.node[edgep[1][0],edgep[1][1]].values())
                common=0
                for k in range(0,F): 
                    if atrs[k]==atro[k]:
                        common=common+1
                if common==0 or common==F:
                    actlinks[y1]=0
                else:
                    actlinks[y1]=1
    #tengo que poner los links que se unen por caracteristicas diferentes para
    #estado absorbente 
#Begin the dynamics 
    t=0 
    dens=sum(actlinks)/len(actlinks)           
    while dens<1 and dens>0:
        i3=rd.randint(0,L*(L-1))
        i2=int(np.mod(i3,L))
        i1=int((i3-i2)/L)
        vec=list(G.neighbors((i1,i2)))
        obj=rd.choice(vec)
        feat=rd.randint(0,F-1)
        if G.node[i1,i2][(feat)]==G.node[obj[0],obj[1]][(feat)]:
            feat2=rd.randint(0,F-1)
            while feat2==feat:
                feat2=rd.randint(0,F-1)
            G.node[i1,i2][(feat2)]=G.node[obj[0],obj[1]][(feat2)]
            
            atrs=list(G.node[i1,i2].values())
            atro=list(G.node[obj[0],obj[1]].values())
            common=0
            for k in range(0,F): 
                    if atrs[k]==atro[k]:
                        common=common+1
            if common==0 or common==F:
                    actlinks[i3]=0
            
            dens=sum(actlinks)/len(actlinks)
            #print(dens)
            t=t+1
    #Choose attribute to compare 
    for k in range(0,F):
        for p3 in range(0,L*(L)):
                p2=int(np.mod(p3,L))
                p1=int((p3-p2)/L)
                colores[p1,p2]=colores[p1,p2]+G.node[p1,p2][k]*10**(k)
    #plb.imshow(colores)


    nodos=list(G.nodes())
    G2=nx.Graph()
    G2.add_nodes_from(nodos)
    for s3 in range(0,L*(L)):
            for o3 in range(0,L*(L)):
                    s2=int(np.mod(s3,L))
                    s1=int((s3-s2)/L)
                    o2=int(np.mod(o3,L))
                    o1=int((o3-o2)/L)
                                        
                    if colores[s1,s2]==colores[o1,o2]:
                        G2.add_edge((s1,s2),(o1,o2))
    giant=max(nx.connected_component_subgraphs(G2),key=len)
    
    smax[indice]=len(giant)/N
    print(q,smax[indice])
    indice=indice+1
    #if indice==2:
    #    sys.exit()


finish=time.time() 
print(finish-start)       