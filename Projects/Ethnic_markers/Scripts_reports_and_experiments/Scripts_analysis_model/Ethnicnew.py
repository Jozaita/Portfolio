##Imports
import numpy as np
import random as rd
##Definitions for statistics
N=100
Ng=2 
agents=[0 for i in range(Ng)]
for i in range(Ng):
    agents[i]=[[0,0,0] for i in range(N)]  ## Behavior, marker, payoff 
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
sim=100         #Numero de simulacions
A=np.zeros([2,2])   #Matriz payoff
A[0,0]=1+delta
A[1,0]=1
A[0,1]=A[1,0]
A[1,1]=A[0,0]
##Definitions for dynamics


for s in range(sim): 
    ##Initial conditions
    for i in range(Ng):
        for j in range(N):
            agents[i][j][0]=rd.randint(0,1)
            agents[i][j][1]=rd.randint(0,1)
    for t in range(tfinal): 
        ##Interaction 
        ## for i in range(Ng)
        part=rd.sample(range(N),2)
        ##Interaction via markers
        a=rd.uniform(0,1)
        if (a<e):
            ##Marker interaction 
            agents2=list(range(N))
            agents2.remove(part[0])
            while (agents[i][part[0]][1]!=agents[i][part[1]][1]):
                part[1]=rd.choice(agents2)
        ##Payoff harvest
        agents[i][part[0]][2]+=A[agents[i][part[0]][0],agents[i][part[1]][0]]
        agents[i][part[0]][2]+=A[agents[i][part[1]][0],agents[i][part[0]][0]]
        ##Adaptation (gamma) 
        if (np.mod(t,gamma*N)==0):
            b=rd.uniform(0,1)
            if(b<r):
                ##Imitation or recombination 
                diffp=agents[i][part[1]][2]-agents[i][part[0]][2]
                if (diffp>0):
                     pcopy=alpha*(diffp)/(delta*agents[i][part[1]][2])
                     c=rd.uniform(0,1)
                     if (c<pcopy):
                         ##Marker and behavior are copied
                         agents[i][part[0]][0]=agents[i][part[1]][0]
                         agents[i][part[0]][1]=agents[i][part[1]][1]             
            else:
                ##Recombination
                agents[i][part[0]][0]=agents[i][part[1]][0]
                agents[i][part[0]][1]=agents[i][part[1]][1] 
                
        ##Migration (beta)
        if (np.mod(t,beta*N)==0):
            lim=int(N*m)
            Migr=[0]*Ng
            for k in range(Ng):
                Migr[k]=rd.sample(range(0,N),lim)
            Migr2=[0]*len(lim)
            for k1 in range(lim):
                Migr2[k1]=agents[0][Migr]
            
