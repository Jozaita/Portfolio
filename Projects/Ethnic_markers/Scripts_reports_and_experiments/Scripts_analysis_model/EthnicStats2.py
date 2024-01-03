
import numpy as np 
import networkx as nx
import random as rd
import time
import sys
from matplotlib import pyplot as plt
sim=50
N=1000             #Número de individuos por grupo
Ng=2                #Número de grupos   
tfinal=500*N
npuntos=200        #numero de puntos por gráfica
Traxec=[0]*Ng*4
Paytemp=[0]*Ng*4
Traxeco=[0]*Ng*4
Paytempo=[0]*Ng*4
tempo=np.arange(tfinal/npuntos,tfinal,tfinal/npuntos)
for i in range(0,4*Ng):
    Traxeco[i]=[0]*(npuntos-1)
    Paytempo[i]=[0]*(npuntos-1)
   
for n in range(0,sim):
    print(n)
    for i in range(0,4*Ng):
            Traxec[i]=[0]*(npuntos-1)
            Paytemp[i]=[0]*(npuntos-1)
    alpha=1          #Factor aceleración de copia            
    delta=0.5        #Recompensa por coordinación
    e=0           #Propensión a interactuar sen marcador 
    r=0             #Rate de recombinación
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
    Migr=[0]*Ng
    #Variábels da dinámica
    mates=[0]*Ng
    ############################################
    #for i in range(0,Ng):
    #    Grupos[i]=[rd.randint(0,1) for i in range(0,N)]
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
                #Actualización //escoller ao mellor//recombinación     
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
                            Traxec[4*i][tp-1]+=1
                            Paytemp[4*i][tp-1]+=Payoff[i][j]/sum(Payoff[i][:])
                        if (Grupos[i][j]==1 and Markers[i][j]==0): 
                            Traxec[4*i+1][tp-1]+=1
                            Paytemp[4*i+1][tp-1]+=Payoff[i][j]/sum(Payoff[i][:])
                        if (Grupos[i][j]==0 and Markers[i][j]==1): 
                            Traxec[4*i+2][tp-1]+=1
                            Paytemp[4*i+2][tp-1]+=Payoff[i][j]/sum(Payoff[i][:])
                        if (Grupos[i][j]==1 and Markers[i][j]==1): 
                            Traxec[4*i+3][tp-1]+=1
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
    #Até este punto temos as traxectorias separadas polas características 
    #Facer un diccionario grupo-->orde. Para depois fazer a estatística sobre
    # a orde
    #Distinguir entre posicións 
    orden=[0]*Ng
    for i in range(0,Ng):
        orden[i]=[0]*4
    for i in range(0,Ng):
        orden[i][0]=Traxec[4*i][-1]
        orden[i][1]=Traxec[4*i+1][-1]
        orden[i][2]=Traxec[4*i+2][-1]
        orden[i][3]=Traxec[4*i+3][-1]
        orden[i]=np.asarray(orden[i])
        orden2=np.argsort(orden)
        orden2[i]=list(orden2[i])
    print(orden)
    #Traducir da orde á Traxeco
    for i in range(0,Ng):
        for j in range(0,npuntos-1):
                Traxeco[4*i][j]+=Traxec[4*i+orden2[i][3]][j]
                Traxeco[4*i+1][j]+=Traxec[4*i+orden2[i][2]][j]
                Traxeco[4*i+2][j]+=Traxec[4*i+orden2[i][1]][j]
                Traxeco[4*i+3][j]+=Traxec[4*i+orden2[i][0]][j]
                Paytempo[4*i][j]+=Paytemp[4*i+orden2[i][3]][j]
                Paytempo[4*i+1][j]+=Paytemp[4*i+orden2[i][2]][j]
                Paytempo[4*i+2][j]+=Paytemp[4*i+orden2[i][1]][j]
                Paytempo[4*i+3][j]+=Paytemp[4*i+orden2[i][0]][j]    
#Estatística
for i in range(0,4*Ng):                    
    for j in range(0,npuntos-1):
       Traxeco[i][j]/=(sim*N)
       Paytempo[i][j]/=sim
#Encontrar orden 
       
#Plots
for i in range(0,Ng):
    fig=plt.figure()
    plt.plot(tempo,Traxeco[4*i],label='1º',c='red')
    plt.plot(tempo,Traxeco[4*i+1],label='2º',c='blue')
    plt.plot(tempo,Traxeco[4*i+2],label='3º',c='green')
    plt.plot(tempo,Traxeco[4*i+3],label='4º',c='purple')
    plt.title('Grupo'+str(i+1)+','+'N='+str(N))
    plt.xlabel('Time')
    plt.ylabel('Agents')
    plt.legend()
    fig.savefig('EMGSt6Group'+str(i+1)+'a='+str(alpha)+'d='+str(delta)
    +'e='+str(e)+'r='+str(r)+'m='+str(m)+'.jpg')
    
for i in range(0,Ng):
    fig=plt.figure()
    plt.plot(tempo,Paytempo[4*i],label='1º',c='red')
    plt.plot(tempo,Paytempo[4*i+1],label='2º',c='blue')
    plt.plot(tempo,Paytempo[4*i+2],label='3º',c='green')
    plt.plot(tempo,Paytempo[4*i+3],label='4º',c='purple')
    plt.title('Grupo'+str(i+1)+','+'N='+str(N))
    plt.xlabel('Time')
    plt.ylabel('Payoff') 
    plt.legend()
    fig.savefig('EMSt6Payoff'+(i+1)+'a='+str(alpha)+'d='+str(delta)
    +'e='+str(e)+'r='+str(r)+'m='+str(m)+'.jpg')