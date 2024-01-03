import numpy as np 
import networkx as nx
import random as rd
import time
import sys
from matplotlib import pyplot as plt
start=time.time()
N=500            #Número de individuos por grupo
agentes=set(range(N))
Ng=2  
tfinal=1500*N
npuntos=50         #numero de puntos por gráfica
tempo=np.arange(tfinal/npuntos,tfinal,tfinal/npuntos) 
tempo/=N  
delta=0.5        #Recompensa por coordinación
alpha=delta          #Factor aceleración de copia
beta=1          #Frecuencia da migración (en unidades de poboación)
gamma=1         #Frecuencia da actualización (en unidades de poboación )            

e=1            #Propensión a interactuar sen marcador 
r=0            #Rate de recombinación
m=0           #Rate migración
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
#################################3
for i in range(0,Ng):
    Grupos[i]=[rd.randint(0,1) for i in range(0,N)]
    Payoff[i]=[0]*N
    Markers[i]=[rd.randint(0,1) for i in range(0,N)]   
#Grupos[0]=int(0.45*N)*[0]+int(0.55*N)*[1]
#rd.shuffle(Grupos[0])
#Grupos[1]=int(0.55*N)*[0]+int(0.45*N)*[1]
#rd.shuffle(Grupos[1])
#Markers[0]=int(0.8*N)*[0]+int(0.2*N)*[1]
#rd.shuffle(Markers[0])
#Markers[1]=int(0.7*N)*[0]+int(0.3*N)*[1]
#rd.shuffle(Markers[1])
################################3
#for i in range(0,Ng):
#    Payoff[i]=[0]*N
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
                k=0
                while ((Markers[i][mates[i][1]]!=Markers[i][mates[i][0]])and(k<10)):
                    mates[i][1]=rd.choice(list(agentes - {mates[i][0]}))
                    k=k+1
            Payoff[i][mates[i][0]]+=A[Grupos[i][mates[i][0]],Grupos[i][mates[i][1]]]
            Payoff[i][mates[i][1]]+=A[Grupos[i][mates[i][1]],Grupos[i][mates[i][0]]]
            #Reconto de grupos, comportamentos e payoffs
            if (np.mod(t,tfinal/npuntos)==0 and t>0):
                tp=round(t/tfinal*npuntos)
                for j in range(0,N):
                    if (Grupos[i][j]==0 and Markers[i][j]==0): 
                        Traxec[4*i][tp-1]+=1/N
                        Paytemp[4*i][tp-1]+=Payoff[i][j]/(sum(Payoff[i][:]))
                    if (Grupos[i][j]==1 and Markers[i][j]==0): 
                        Traxec[4*i+1][tp-1]+=1/N
                        Paytemp[4*i+1][tp-1]+=Payoff[i][j]/(sum(Payoff[i][:]))
                    if (Grupos[i][j]==0 and Markers[i][j]==1): 
                        Traxec[4*i+2][tp-1]+=1/N
                        Paytemp[4*i+2][tp-1]+=Payoff[i][j]/(sum(Payoff[i][:]))
                    if (Grupos[i][j]==1 and Markers[i][j]==1): 
                        Traxec[4*i+3][tp-1]+=1/N
                        Paytemp[4*i+3][tp-1]+=Payoff[i][j]/(sum(Payoff[i][:]))       
                        
        #Actualización //escoller ao mellor//recombinación     
        if np.mod(t,gamma*N)==0:
            for j in range(Ng):
                for i in range(N):
                    mates[j][0]=i
                    b=rd.uniform(0,1)    
                    mates[j][1]=rd.choice(list(agentes - {mates[j][0]}))
                    if (b<r): #Cópiase por recombinación
                        Grupos[j][mates[j][0]]=Grupos[j][mates[j][1]]
                        Markers[j][mates[j][0]]=Markers[j][mates[j][1]]
                    else:  #Cópiase por imitación ó millor
                        diffp=Payoff[j][mates[j][1]]-Payoff[j][mates[j][0]]
                        if (diffp>0):
                            pcopy=alpha*(diffp)/(delta*Payoff[j][mates[j][1]])
                            c=rd.uniform(0,1)
                            if (c<pcopy):
                                Grupos[j][mates[j][0]]=Grupos[j][mates[j][1]]
                                Markers[j][mates[j][0]]=Markers[j][mates[j][1]]        
        #Migración
        if np.mod(t,beta*N)==0:
            
            lim=int(N*m)
            for j in range(0,Ng):
                Migr[j]=rd.sample(range(0,N),lim)
            
            #Organización das fronteiras, neste caso 
            #cada grupo copia ó da dereita
            temp=[0]*N
            temp2=[0]*N
            temp3=[0]*N
            for i in range(0,N):
                temp[i]=Grupos[0][i]
                temp2[i]=Markers[0][i]            
                temp3[i]=Payoff[0][i]
            
            for j in range(0,Ng-1):
                for k in range(0,lim):
                    Markers[j][Migr[j][k]]=Markers[j+1][Migr[j+1][k]]
                    Grupos[j][Migr[j][k]]=Grupos[j+1][Migr[j+1][k]]
                    Payoff[j][Migr[j][k]]=Payoff[j+1][Migr[j+1][k]]
            for k in range(0,lim):
                Grupos[-1][Migr[-1][k]]=temp[Migr[0][k]]
                Markers[-1][Migr[-1][k]]=temp2[Migr[0][k]]
                Payoff[-1][Migr[-1][k]]=temp3[Migr[0][k]]
print(Markers[0].count(0)+Markers[1].count(0),Markers[0].count(1)+Markers[1].count(1))
           
#Plots
line=['-','--']
color=[['red','blue'],['darksalmon','mediumpurple']]
label=[['G1 Circle 0','G1 Circle 1','G1 Triangle 0','G1 Triangle 1'],
       ['G2 Circle 0','G2 Circle 1','G2 Triangle 0','G2 Triangle 1']]
fig=plt.figure()
for i in range(0,Ng):
    
    plt.ticklabel_format(axis='x',syle='sci')
    plt.plot(tempo,Traxec[4*i],label=label[i][0],
             linestyle=line[i],c=color[i][0],marker='o')
    plt.plot(tempo,Traxec[4*i+1],label=label[i][1],
             linestyle=line[i],c=color[i][1],marker='o')
    plt.plot(tempo,Traxec[4*i+2],label=label[i][2],
             linestyle=line[i],c=color[i][0],marker='^')
    plt.plot(tempo,Traxec[4*i+3],label=label[i][3],
             linestyle=line[i],c=color[i][1],marker='^')
    plt.title('Grupos,'+'N='+str(N))
    plt.xlabel('Time/N')
    plt.ylabel('Agents')
    plt.legend()
    fig.savefig('EMAg_Pr,N='+str(N)+'b='+str(beta)+'d='+str(delta)
    +'e='+str(e)+'r='+str(r)+'m='+str(m)+'.jpg')
    
    
fig=plt.figure()    
for i in range(0,Ng):
    
    plt.ticklabel_format(axis='x',syle='sci')
    plt.plot(tempo,Paytemp[4*i],label=label[i][0],
             linestyle=line[i],c=color[i][0],marker='o')
    plt.plot(tempo,Paytemp[4*i+1],label=label[i][1],
             linestyle=line[i],c=color[i][1],marker='o')
    plt.plot(tempo,Paytemp[4*i+2],label=label[i][2],
             linestyle=line[i],c=color[i][0],marker='^')
    plt.plot(tempo,Paytemp[4*i+3],label=label[i][3],
             linestyle=line[i],c=color[i][1],marker='^')
    plt.title('Payoff,'+'N='+str(N))
    plt.xlabel('Time/N')
    plt.ylabel('Agents')
    plt.legend()
    fig.savefig('EMPay_Pr,N='+str(N)+'b='+str(beta)+'d='+str(delta)
    +'e='+str(e)+'r='+str(r)+'m='+str(m)+'.jpg')
print(time.time()-start)    


    
#for i in range(0,Ng):
    

