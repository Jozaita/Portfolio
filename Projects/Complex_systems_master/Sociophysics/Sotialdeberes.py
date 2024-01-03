import numpy as np 
import networkx as nx
import random as rd
import time
import sys
from matplotlib import pyplot as plb
#Condiciones de la poblacion
N=10**1
t=1
tfinal=10**6 
opmax=9
giant=[0]*(opmax-2)

mu=3
states=[0]*mu
agentes=[i for i in range(0,N)]
start=time.time()
for op in range(2,opmax):
    for j in range(0,len(states)):
        #states[j]=rd.choice([i for i in range(2,10)])
        states[j]=op
    colores=[0]*N
    dicdens={}
    
    #Definimos la grafica y ponemos el estado inicial 
    G=nx.complete_graph(N)
    G.add_nodes_from(agentes)
    for j in range(0,mu):
        for i in range(0,N):
            G.node[i][str(j)]=rd.choice([i for i in range(1,states[j])])
    
            dicdens[j]=[G.nodes(data=str(j))[i] for i in  range(0,N)] 

#Dinamica
    for t in range(0,tfinal):
        common=0
        i=rd.choice(agentes)
        j=rd.choice(list(G.neighbors(i)))
        for k in range(0,len(states)):
            if dicdens[k][i]==dicdens[k][j]:
                common=common+1
        p=common/mu
    
    q=rd.uniform(0,1)
    if q<p:
        q2=rd.choice(range(0,mu-1))
        if G.node[j][str(q2)]==G.node[i][str(q2)]:
            q2=rd.choice(range(0,mu-1))
        dicdens[q2][j]=dicdens[q2][ i]
        G.node[j][str(q2)]=G.node[i][str(q2)]
         

    for j in agentes:
        for k in range(0,mu):    
            colores[j]=colores[j]+dicdens[k][j]*10**(k)
        
#Analisis de la network
    G2=nx.Graph()
    G2.add_nodes_from(agentes)
    for j in range(0,len(agentes)-1):
        for k in range(0,len(agentes)):
            if colores[j]==colores[k]:
                G2.add_edge(j,k)
    giant[op-2]=max(nx.connected_component_subgraphs(G2),key=len)
    giant[op-2]=len(giant)/N




final=time.time()
print(final-start)