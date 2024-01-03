####Imports
import numpy as np
import random as rd
import time
from matplotlib import pyplot as plt
import heapq
####Definitions
start=time.time()
N=400
Ng=2
tfinal=N*100*4
delta=0.5
gamma=1/N
beta=1
alpha=delta
e=1
r=0
m=0.025
npuntos=N
A=np.zeros([2,2])   #Payoff matrix
A[0,0]=1+delta
A[1,0]=1
A[0,1]=A[1,0]
A[1,1]=A[0,0]
final2=[[0]*npuntos for i in range(Ng)]
####Functions 
def interact(a,b):
    a[3]+=A[a[1],b[1]]
    b[3]+=A[b[1],a[1]]
    return
def update(a,b):
    a[1]=b[1]
    a[2]=b[2]
    return
def migrate(a,lim):
    for j in range(Ng):
        subset3=[a[i] for i in range(N) if a[i][0]==j]
        sample=rd.sample(subset3,lim)
        for i in range(lim):
            sample[i][0]+=1
            if (sample[i][0]==Ng): sample[i][0]=0
    return 
    


###Circunstantial conditions
agents=[[0]*4 for i in range(N)]
for i in range(N):
    agents[i][0]=int(i//(N/Ng))
    agents[i][1]=rd.randint(0,1)
    agents[i][2]=rd.randint(0,1)

###Dynamics starts
for t in range(tfinal):
        
    for j in range(Ng):
        ##Interaction phase
        subset=[agents[i] for i in range(N) if agents[i][0]==j]
        subj=rd.choice(subset)
        subset.remove(subj)
        a1=rd.uniform(0,1)
        if (a1>e):
            ##Marker interaction, olla o asunto dos parametros
            subset2=[subset[i] for i in range(len(subset)) if subset[i][2]==subj[2]]
            if (len(subset2)>0): 
                obj=rd.choice(subset2)
                interact(subj,obj)
            
        else:
            ##Non-marker interaction 
            obj=rd.choice(subset)
            interact(subj,obj)
        ##Update phase    
        if (np.mod(t,gamma*N)==0):
            obj=rd.choice(subset)
            a2=rd.uniform(0,1)
            if (a2<r): ##Update by recombination
                update(subj,obj)
            else: ##Update by imitation
                 diffp=obj[3]-subj[3]
                 if (diffp>0):
                     pcopy=alpha*(diffp)/(delta*obj[3])
                     a3=rd.uniform(0,1)
                     if (a3<pcopy):
                         update(subj,obj)
        ##Migrate phase
        if (np.mod(t,beta*N)==0):
            lim=int(N*m)
            migrate(agents,lim)
        ##Anotation phase
        if (np.mod(t,tfinal/npuntos)==0):
            final=[[0]*np.size(A) for i in range(Ng)]
            for v1 in range(Ng):
                k1=0
                subset3=[agents[i] for i in range(N) if agents[i][0]==v1]
                for i1 in range(len(A)):
                    for j1 in range(len(A)):
                        final[v1][k1]=len([subset3[i] for i in range(len(subset3)) if ((subset3[i][1]==i1)and(subset3[i][2]==j1))])/(N/Ng)
                        k1=k1+1
                final2[v1][round(t/tfinal*npuntos)]=final[v1]
###Measures after one dynamics is complete 
###Find order parameter for an evaluation


    
    #final.index(chosen[0])
    #final.index(chosen[1])
print(time.time()-start)    

    
    