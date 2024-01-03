import numpy as np 
import networkx as nx
import random as rd
import time
import sys
from matplotlib import pyplot as plt
tfinal=100
N=100                  #Número de individuos por grupo 
delta=0.5              #Recompensa por coordinación
e=0.5                     #Propensión a interactuar sin marcador 
r=0.1                    #Rate de recombinación
A=np.zeros([2,2])   #Matriz payoff
A[0,0]=1+delta
A[1,0]=1
A[0,1]=A[1,0]
A[1,1]=A[0,0]

G1=[0]*N          #Definir grupos 
pay1=[0]*N
mark1=[0]*N           
G2=[0]*N
pay2=[0]*N
mark2=[0]*N 
unos1=[]
unos2=[]
ceros1=[]
ceros2=[]
for i in range(0,N):     #Puesta a punto de grupos
    G1[i]=rd.randint(0,1)
    mark1=rd.randint(0,1)
    G2[i]=rd.randint(0,1)
    mark2=rd.randint(0,1)
    
#Empezamos la dinámica 
for t in range(0,tfinal):
    for j in range(0,N):
        suj=j
        suj2=j
        a=rd.uniform(0,1)
        if (a<e):   #Interacción por markers
            obj=rd.randint(0,N)
            obj2=rd.randint(0,N)
            #Grupo1
            if (mark1[obj]==mark1[suj]): 
                pay1[suj]+=A[G1[suj],G1[obj]]
            else:
                while(mark1[obj]!=mark1[obj]):
                    obj=rd.randint(0,N)
                pay1[suj]+=A[G1[suj],G1[obj]]
            #Grupo2 
            if (mark2[obj2]==mark2[suj2]): 
                pay2[suj2]+=A[G2[suj2],G2[obj2]]
            else:
                while(mark2[obj2]!=mark2[obj2]):
                    obj2=rd.randint(0,N)
                pay2[suj2]+=A[G2[suj2],G2[obj2]]
                
        else:  #Interacción en general 
            obj=rd.randint(0,N)
            obj2=rd.randint(0,N)
            pay1+=A[G1[suj],G1[obj]]
            pay2+=A[G2[suj2],G2[obj2]]
    #Copiar comportamientos (recombinación/imitación)
    for j in range(0,N):
        a=rd.uniform(0,1)
        if(a<r): #Se copia por recombinación
            