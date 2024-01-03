####Imports
import numpy as np
import random as rd
import time
from matplotlib import pyplot as plt
import heapq
####Definitions
start=time.time()
N=200
Ng=2
tfinal=4*N*10**2
delta=0.5
gamma=1/N
beta=1
alpha=delta
e=0 
r=0.01
m=0
sim=1
A=np.zeros([2,2])   #Payoff matrix
A[0,0]=1+delta
A[1,0]=1
A[0,1]=A[1,0]
A[1,1]=A[0,0]
orderin=[0]*sim 
orderout=[0]*sim
dif=[0]*sim
meanpay=[[0]*401 for i in range(2)]
varpay=[[0]*401 for i in range(2)]
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
def intragroup(final,args):
    intraorder=[[0,0] for i in range(Ng)]
    for i in range(Ng):
        intraorder[i][0]=max(final[i])
        intraorder[i][1]=sum(args[i])
        if (intraorder[i][1]==3):
            intraorder[i][1]=-1
        else:
            intraorder[i][1]=np.mod(intraorder[i][1],2)
    return intraorder
def intergroup(args):
    interorder=0
    for i in range(Ng):
        interorder+=args[i][0] 
    if (interorder==3):
        interorder=1
    elif (args[0][0]==args[1][0]):
        interorder=0        ###Esto no vale para mas de 2 grupos
    else:
        interorder=np.mod(interorder,2)
    return interorder    
##Parameter dependent arrays
#res=np.arange(0,0.1,0.01)
#for e in range(0,0.1,0.25)
for s in range(sim):
###Circunstantial conditions
    agents=[[0]*4 for i in range(N)]
    for i in range(N):
        agents[i][0]=int(i//(N/Ng))
        agents[i][1]=rd.randint(0,1)
        agents[i][2]=rd.randint(0,1)
        if(agents[i][1]==1): agents[i][3]=100
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
            ##Measures during the dynamics
            if(np.mod(t,N)):
                t1=round(t/N+0.1)
                for i3 in range(2):
                    meanpay[i3][t1]=np.mean([agents[i][3] for i in range(N) if agents[i][0]==0 and agents[i][2]==i3])
                    varpay[i3][t1]=np.std([agents[i][3] for i in range(N) if agents[i][0]==0 and agents[i][2]==i3])
    ###Measures after one dynamics is complete 
    ###Find order parameter for an evaluation
    final=[[0]*np.size(A) for i in range(Ng)]
    chosen=[0]*Ng
    args=[[0]*2 for i in range(Ng)]
    for v1 in range(Ng):
        k1=0
        subset3=[agents[i] for i in range(N) if agents[i][0]==v1]
        for i1 in range(len(A)):
            for j1 in range(len(A)):
                final[v1][k1]=len([subset3[i] for i in range(len(subset3)) if ((subset3[i][1]==i1)and(subset3[i][2]==j1))])/(N/Ng)
                k1=k1+1
        chosen[v1]=heapq.nlargest(2,final[v1])
        for i in range(len(chosen[v1])):    
            args[v1][i]=final[v1].index(chosen[v1][i])
        #####Functions of order parameter inter and intra group
        orderin[s]=intragroup(final,args)
        orderout[s]=intergroup(args)
    

print(time.time()-start)    
   
    
    
    