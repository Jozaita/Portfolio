import numpy as np 
import networkx as nx
import random as rd
import time
import sys
from matplotlib import pyplot as plt
start=time.time()
N=1000              #Número de individuos por grupo
Ng=2  
tfinal=500*N
npuntos=200         #numero de puntos por gráfica
sim=50
Traxeco=[0]*Ng*4
Paytempo=[0]*Ng*4
tempo=np.arange(tfinal/npuntos,tfinal,tfinal/npuntos) 
for i in range(0,4*Ng):
    Traxeco[i]=[0]*(npuntos-1)
    Paytempo[i]=[0]*(npuntos-1)
for n in range(0,sim):  
    print(n)    
    alpha=1          #Factor aceleración de copia            
    delta=0.5        #Recompensa por coordinación
    e=0.25            #Propensión a interactuar sen marcador 
    r=0.1              #Rate de recombinación
    m=0.025             #Rate migración
    A=np.zeros([2,2])   #Matriz payoff
    A[0,0]=1+delta
    A[1,0]=1
    A[0,1]=A[1,0]
    A[1,1]=A[0,0]
    #Definición de grupos e atributos
    Grupos=[0]*Ng
    Payoff=[0]*Ng
    Markers=[0]*Ng
    Traxec=[0]*Ng*4
    Paytemp=[0]*Ng*4
    Migr=[0]*Ng
    #Variábels da dinámica
    mates=[0]*Ng
    #Condicións iniciais 
    #for i in range(0,Ng):
    #   Grupos[i]=[rd.randint(0,1) for i in range(0,N)]
    #    Payoff[i]=[0]*N
    #    Markers[i]=[rd.randint(0,1) for i in range(0,N)]  
    for i in range(0,Ng):
        Grupos[i]=int(0.45*N)*[0]+int(0.55*N)*[1]
        rd.shuffle(Grupos[i])
        Payoff[i]=[0]*N
    Markers[0]=int(0.2*N)*[0]+int(0.8*N)*[1]
    rd.shuffle(Markers[0])
    Markers[1]=int(0.3*N)*[0]+int(0.7*N)*[1]
    rd.shuffle(Markers[1])
    ##############################
    for i in range(0,4*Ng):
        Traxec[i]=[0]*(npuntos-1)
        Paytemp[i]=[0]*(npuntos-1)
    #Comeza a dinámica
    for t in range(0,tfinal):
            for i in range(0,Ng):
                mates[i]=rd.sample(range(0,N),2)
                a=rd.uniform(0,1)
                #Interacción por markers
                if (a>e): 
                    while (Markers[i][mates[i][1]]!=Markers[i][mates[i][0]]):
                        mates[i][1]=rd.randint(0,N-1)                    
                Payoff[i][mates[i][0]]+=A[Grupos[i][mates[i][0]],Grupos[i][mates[i][1]]]
                Payoff[i][mates[i][1]]+=A[Grupos[i][mates[i][1]],Grupos[i][mates[i][0]]]
                #Actualización //escoller o mellor//recombinación     
                b=rd.uniform(0,1)    
                mates[i][1]=rd.randint(0,N-1)
                while(mates[i][1]==mates[i][0]):
                        mates[i][1]=rd.randint(0,N-1)
                if (b<r): #Cópiase por recombinación
                    Grupos[i][mates[i][0]]=Grupos[i][mates[i][1]]
                    Markers[i][mates[i][0]]=Markers[i][mates[i][1]]
                else:  #Cópiase por imitación ó millor
                    diffp=Payoff[i][mates[i][1]]-Payoff[i][mates[i][0]]
                    if (diffp>0):
                        pcopy=alpha*(diffp)/(delta*Payoff[i][mates[i][1]])
                        c=rd.uniform(0,1)
                        if (c<pcopy):
                           Grupos[i][mates[i][0]]=Grupos[i][mates[i][1]]
                           Markers[i][mates[i][0]]=Markers[i][mates[i][1]] 
            
                #Reconto de grupos, comportamentos e payoffs
                if (np.mod(t,tfinal/npuntos)==0 and t>0):
                    tp=round(t/tfinal*npuntos)
                    
                    for j in range(0,N):
                        if (Grupos[i][j]==0 and Markers[i][j]==0): 
                            Traxec[4*i][tp-1]+=1/N
                            Paytemp[4*i][tp-1]+=Payoff[i][j]/sum(Payoff[i][:])
                        if (Grupos[i][j]==1 and Markers[i][j]==0): 
                            Traxec[4*i+1][tp-1]+=1/N
                            Paytemp[4*i+1][tp-1]+=Payoff[i][j]/sum(Payoff[i][:])
                        if (Grupos[i][j]==0 and Markers[i][j]==1): 
                            Traxec[4*i+2][tp-1]+=1/N
                            Paytemp[4*i+2][tp-1]+=Payoff[i][j]/sum(Payoff[i][:])
                        if (Grupos[i][j]==1 and Markers[i][j]==1): 
                            Traxec[4*i+3][tp-1]+=1/N
                            Paytemp[4*i+3][tp-1]+=Payoff[i][j]/sum(Payoff[i][:])
            
            #Migración
            if np.mod(t,N)==0:
                lim=int(N*m)
                for j in range(0,Ng):
                    Migr[j]=rd.sample(range(0,N),lim)
                #Organización das fronteiras, neste caso 
                #cada grupo copia ó da dereita
                temp=Grupos[-1]
                temp2=Markers[-1]
                for j in range(1,Ng):
                    for k in range(0,lim):
                        Markers[j][Migr[j][k]]=Markers[j-1][Migr[j-1][k]]
                        Grupos[j][Migr[j][k]]=Grupos[j-1][Migr[j-1][k]]
                for k in range(0,lim):
                    Grupos[0][Migr[0][k]]=temp2[k]
                    Markers[0][Migr[0][k]]=temp[k]
    for i in range(0,Ng):
       for j in range(0,npuntos-1):
                Traxeco[4*i][j]+=Traxec[4*i][j]
                Traxeco[4*i+1][j]+=Traxec[4*i+1][j]
                Traxeco[4*i+2][j]+=Traxec[4*i+2][j]
                Traxeco[4*i+3][j]+=Traxec[4*i+3][j]
                Paytempo[4*i][j]+=Paytemp[4*i][j]
                Paytempo[4*i+1][j]+=Paytemp[4*i+1][j]
                Paytempo[4*i+2][j]+=Paytemp[4*i+2][j]
                Paytempo[4*i+3][j]+=Paytemp[4*i+3][j]
    print(Traxec[0][-1],Traxec[1][-1],Traxec[2][-1],Traxec[3][-1])            
for i in range(0,4*Ng):                    
    for j in range(0,npuntos-1):
       Traxeco[i][j]/=sim
       Paytempo[i][j]/=sim
#Plots
for i in range(0,Ng):
    fig=plt.figure(figsize=(10,8))
    plt.plot(tempo,Traxeco[4*i],label='Circles,0')
    plt.plot(tempo,Traxeco[4*i+1],label='Circles 1')
    plt.plot(tempo,Traxeco[4*i+2],label='Triangles 0')
    plt.plot(tempo,Traxeco[4*i+3],label='Triangles 1')
    plt.title('Grupo'+str(i+1)+','+'N='+str(N))
    plt.xlabel('Time')
    plt.ylabel('Agents')
    plt.legend()
    fig.savefig('EMStGroup'+str(i+1)+'a='+str(alpha)+'d='+str(delta)
    +'e='+str(e)+'r='+str(r)+'m='+str(m)+'.jpg')
    
for i in range(0,Ng):
    fig=plt.figure(figsize=(10,8))
    plt.plot(tempo,Paytempo[4*i],label='Circles 0')
    plt.plot(tempo,Paytempo[4*i+1],label='Circles 1')
    plt.plot(tempo,Paytempo[4*i+2],label='Triangles 0')
    plt.plot(tempo,Paytempo[4*i+3],label='Triangles 1')
    plt.title('Grupo'+str(i+1)+','+'N='+str(N))
    plt.xlabel('Time')
    plt.ylabel('Payoff') 
    plt.legend()
    fig.savefig('EMStPayoff'+str(i+1)+'a='+str(alpha)+'d='+str(delta)
    +'e='+str(e)+'r='+str(r)+'m='+str(m)+'.jpg')
finish=time.time()    
print(finish-start)

    
#for i in range(0,Ng):
    

