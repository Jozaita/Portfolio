import numpy as np 
import networkx as nx
import random as rd
import time
import sys
from matplotlib import pyplot as plt
N=250              #Número de individuos por grupo  
tfinal=50*N      
##########################3
c0=[0]*tfinal
c1=[0]*tfinal
t0=[0]*tfinal
t1=[0]*tfinal
c20=[0]*tfinal
c21=[0]*tfinal
t20=[0]*tfinal
t21=[0]*tfinal
pc0=[0]*tfinal
pc1=[0]*tfinal
pt0=[0]*tfinal
pt1=[0]*tfinal 
pc20=[0]*tfinal
pc21=[0]*tfinal
pt20=[0]*tfinal
pt21=[0]*tfinal 
####################3  
alpha=1          #Factor aceleración de copia            
delta=0.5        #Recompensa por coordinación
e=0.1            #Propensión a interactuar sin marcador 
r=0.1              #Rate de recombinación
m=0             #Rate migración
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
for i in range(0,N):     #Puesta a punto de grupos
    G1[i]=rd.randint(0,1)
    mark1[i]=rd.randint(0,1)
    G2[i]=rd.randint(0,1)
    mark2[i]=rd.randint(0,1)
    
#Empezamos la dinámica 
for t in range(0,tfinal):
        mates=rd.sample(range(0,N),2)
        mates2=rd.sample(range(0,N),2)
        suj=mates[0]
        obj=mates[1]
        suj2=mates2[0]
        obj2=mates2[1]
        a=rd.uniform(0,1)
        #Interacción 
        if (a<e):   #Interacción por markers
            #Grupo1
            if (mark1[obj]==mark1[suj]): 
                pay1[suj]+=A[G1[suj],G1[obj]]
                pay1[obj]+=A[G1[obj],G1[suj]]
            else:
                while(mark1[suj]!=mark1[obj]):
                    obj=rd.randint(0,N-1)
                pay1[suj]+=A[G1[suj],G1[obj]]
                pay1[obj]+=A[G1[obj],G1[suj]]
            #Grupo2 
            if (mark2[obj2]==mark2[suj2]): 
                pay2[suj2]+=A[G2[suj2],G2[obj2]]
                pay2[obj2]+=A[G2[obj2],G2[suj2]]
            else:
                while(mark2[suj2]!=mark2[obj2]):
                    obj2=rd.randint(0,N-1)
                pay2[suj2]+=A[G2[suj2],G2[obj2]]
                pay2[obj2]+=A[G2[obj2],G2[suj2]]
        else:  #Interacción en general 
            pay1[suj]+=A[G1[suj],G1[obj]]
            pay1[obj]+=A[G1[obj],G1[suj]]
            pay2[suj2]+=A[G2[suj2],G2[obj2]]
            pay2[obj2]+=A[G2[obj2],G2[suj2]]
        #Actualizar vector proportional imitation 
        probcopia=[0]*(N+1)
        probcopia2=[0]*(N+1)
        probcopia[0]=0
        probcopia2[0]=0
        for i in range(1,N+1):
            probcopia[i]=probcopia[i-1]+pay1[i-1]/sum(pay1)
            probcopia2[i]=probcopia[i-1]+pay2[i-1]/sum(pay2)
        #Copiar comportamientos (recombinación/imitación)
        for j in range(0,N):
            a=rd.uniform(0,1)
            a2=rd.uniform(0,1)
            if(a<r): #Se copia por recombinación en grupo 1
                objr=rd.randint(0,N-1)
                while (objr==suj):
                    objr=rd.randint(0,N-1)
                G1[suj]=G1[objr]
                mark1[suj]=mark1[objr]
            else: #Se copia al mejor en grupo 1
               objc=rd.randint(0,N-1)
               diffp=pay1[objc]-pay1[suj]
               if (diffp>0):
                   pcopy=alpha*(N/t)*(diffp)/delta
                   b=rd.uniform(0,1)
                   if (b<pcopy): 
                       G1[suj]=G1[objc]
                       mark1[suj]=mark1[objc]
               # Simplificamos directamente la dif entre payoff
               
            if(a2<r):  #Recombinación grupo 2
                objr2=rd.randint(0,N-1)
                while (objr2==suj2):
                    objr2=rd.randint(0,N-1)
                G2[suj2]=G2[objr2]
                mark2[suj2]=mark2[objr2]
            else: #Se copia al mejor grupo 2 
                objc2=rd.randint(0,N-1)
                diffp2=pay2[objc2]-pay2[suj2]
                if (diffp2>0):
                   pcopy2=alpha*(N/t)*(diffp2)/delta
                   b2=rd.uniform(0,1)
                   if (b2<pcopy2): 
                       G2[suj2]=G2[objc2]
                       mark2[suj2]=mark2[objc2]
        #Recuento de marcadores,comportamientos y payoffs

        for k in range(0,N):
            if (G1[k]==0 and mark1[k]==0): 
                c0[t]+=1
                pc0[t]+=pay1[k]
            if (G1[k]==1 and mark1[k]==0): 
                c1[t]+=1 
                pc1[t]+=pay1[k]
            if (G1[k]==0 and mark1[k]==1): 
                t0[t]+=1
                pt0[t]+=pay1[k]
            if (G1[k]==1 and mark1[k]==1): 
                t1[t]+=1 
                pt1[t]+=pay1[k]
            if (G2[k]==0 and mark2[k]==0): 
                c20[t]+=1
                pc20[t]+=pay2[k]
            if (G2[k]==1 and mark2[k]==0): 
                c21[t]+=1 
                pc21[t]+=pay2[k]
            if (G2[k]==0 and mark2[k]==1): 
                t20[t]+=1 
                pt20[t]+=pay2[k]
            if (G2[k]==1 and mark2[k]==1): 
                t21[t]+=1 
                pt21[t]+=pay2[k]
           
        
        #Migración
        if np.mod(t,N)==0:
            lim=int(N*m)
            migr=rd.sample(range(0,N),lim)
            migr2=rd.sample(range(0,N),lim)
            temp=G1
            temp2=mark1
            h=0
            for i in migr:
                G1[i]=G2[migr2[h]]
                G2[migr2[h]]=temp[i] 
                mark1[i]=mark2[migr2[h]]
                mark2[migr2[h]]=temp2[i]
                h=h+1

f1=plt.figure()
plt.plot(c0,label='Circles 0')
plt.plot(c1,label='Circles 1')
plt.plot(t0,label='Triangles 0')
plt.plot(t1,label='Triangles 1')
plt.title('Grupo 1')
plt.legend()     
f1.savefig('Ethnic1.jpg')
f2=plt.figure()
plt.plot(c20,label='Circles 0')
plt.plot(c21,label='Circles 1')
plt.plot(t20,label='Triangles 0')
plt.plot(t21,label='Triangles 1')
plt.title('Grupo 2')
plt.legend() 
f2.savefig('Ethnic2.jpg')
f3=plt.figure()
plt.plot(pc0,label='Payoff Circles 0')
plt.plot(pc1,label='Payoff Circles 1')
plt.plot(pt0,label='Payoff Triangles 0')
plt.plot(pt1,label='Payoff Triangles 1')
plt.title('Payoff Grupo 1')
plt.legend()
f3.savefig('Group 1 payoff.jpg')
f4=plt.figure()
plt.plot(pc20,label='Payoff Circles 0')
plt.plot(pc21,label='Payoff Circles 1')
plt.plot(pt20,label='Payoff Triangles 0')
plt.plot(pt21,label='Payoff Triangles 1')
plt.title('Grupo 2')
plt.legend()
f4.savefig('Group 2 payoff.jpg')