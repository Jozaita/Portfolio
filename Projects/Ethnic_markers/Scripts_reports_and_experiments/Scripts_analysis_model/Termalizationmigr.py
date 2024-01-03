##imports
import random as rd
import numpy as np
import time
from matplotlib import pyplot as plt
from scipy import stats
import math
##Simulation variables
start=time.time()
N=500
T=25000
delta=0.5
delta1=0
h1=0
e=0.5
h=0
l=0.5
beta=0.1
m=0.002
lim=int(m*N)
pdif=4 #number of different probabilities (2xbehaviours)
bins=np.linspace(0,1,50)

A=np.zeros([2,2])   #Payoff matrix
A[0,0]=1+delta+delta1
A[0,1]=1-h1
A[1,0]=1
A[1,1]=1+delta
Ng=2
##Agents variables
agents=[[0]*7 for i in range(N)] ##(beh,mar,pay,int,asp,group,nmigr)
prob=[[0]*pdif for i in range(N)]##(p=a,p=b,p!a,p!b)
stim=[0]*2

action=[0]*2
a=[0]*2
aspirations=[1.1]
uasp=list(np.unique(aspirations))
sample=[0]*Ng
num=int(math.factorial(len(uasp)+1)/(math.factorial(len(uasp)-1)*2))
stimula=[[0]*num for i in range(Ng)]
#stimulatemp=[[0]*Ng for i in range(int(T/N))]
stimulatemp=[[0]*Ng for i in range(1000)]
##Correlation and CI vector 
heat=[np.zeros((len(bins)-1,len(bins)-1)) for i in range(Ng+1)]
corrvec=[[0,0] for i in range(Ng+1)]
corrfactor=[[0,0] for i in range(Ng+1)]
civec=[[0]*100 for i in range(Ng+1)]
####Cutoff for pearsonR
cutoff=10**(-2)
##Functions
def interact(a,b):
    a[3]+=1
    b[3]+=1
    if(a[0]==b[0]):
        a[2]+=1
        b[2]+=1
    else:
        a[2]+=0
        b[2]+=0
    return
def norm(prob,action):
    if (np.mod(action,2)==0):
        action2=action+1
    else:
        action2=action-1
    prob[action2]=1.0-prob[action]
    return
##Initial conditions
for i in range(N):
    agents[i][0]=rd.randint(0,1)
    agents[i][4]=rd.choice(aspirations)
    agents[i][1]=rd.randint(0,1)
    agents[i][6]=0
    if (i<N/2):
            agents[i][5]=0
    else:
            agents[i][5]=1
    for j in range(pdif):
        if (np.mod(j,2)==0):
            prob[i][j]=rd.uniform(0,1)
        else:
            prob[i][j]=1-prob[i][j-1]

    ####
#for i in range(N):
#    if (agents[i][4]==0.8):
#        prob[i]=[1,0,0.5,0.5]
subset=[[0]*2 for i in range(Ng)]
for k in range(Ng):
    for j in range(2):
        subset[k][j]=[i for i in range(N) if (agents[i][1]==j and agents[i][5]==k)]

##Dynamics
for t in range(T):
    ##Termalization
    if (t==(200*N)):
        for i in range(N):
            agents[i][2]=0
            agents[i][3]=0
    
    for p in range(Ng):
        ##Parameter e
            a11=rd.uniform(0,1)
            if (a11>e): ##Marker interaction, choose field of action
                ##Choose couple
                b=rd.randint(0,1)
                couple=rd.sample(subset[p][b],2)
                ##Choose field of action
                for i in range(2):
                    a[i]=rd.uniform(0,1)
                    action[i]=prob[couple[i]][0]
                    kaux=0
            else: ## Non-marker interaction
                ##Choose couple
                couple=rd.sample(subset[p][0]+subset[p][1],2)
            ##Choose field of action depending on partner's marker
            if (agents[couple[0]][1]==agents[couple[1]][1]):
                for i in range(2):
                    a[i]=rd.uniform(0,1)
                    action[i]=prob[couple[i]][0]
                    kaux=0
            else:
                for i in range(2):
                    a[i]=rd.uniform(1,2)
                    action[i]=1+prob[couple[i]][2]
                    kaux=2
            ##Fago o mesmo para o partner?? Ainda que sexa, teño que preguntarlle óº Anxo
            ##Queda escrito aquí para probalo no testeo,é todo o que leva o 2
       
            for i in range(2):
                k=0+kaux
                while(a[i]>action[i]):
                    k+=1
                    action[i]+=prob[couple[i]][k]
                action[i]=k
                agents[couple[i]][0]=np.mod(action[i],2)
            ####
            #print(action)
            interact(agents[couple[0]],agents[couple[1]])
            ##Collect payoff, calculate aspiration and stimulus
            k=-1
            for i in couple:
                k+=1
                for j in range(2):
                    stim[j]=round(abs(A[j,0]-agents[i][4]),4)
                stimulus=(A[agents[couple[0]][0],agents[couple[1]][0]]-agents[i][4])/max(stim) ##So válido pra xogo de coordinación
                agents[i][4]=(1-h)*agents[i][4]+h*A[agents[couple[0]][0],agents[couple[1]][0]]
                ##Calculate probability update
                if (stimulus>=0):
                    prob[i][action[k]]+=(1-prob[i][action[k]])*l*stimulus
                else:
                    prob[i][action[k]]+=prob[i][action[k]]*l*stimulus
                if (prob[i][action[k]]>1): prob[i][action[k]]=1
                if (prob[i][action[k]]<0): prob[i][action[k]]=0 
                norm(prob[i],action[k])
            stimula[p][uasp.index(agents[couple[0]][-3])+uasp.index(agents[couple[1]][-3])]+=1-stim.index(round(abs(stimulus*max(stim)),4))
            if ((np.mod(t,25)==0) and t>0):
                    for j4 in range(num):   
                        stimulatemp[t//25][p]=stimula[p]
   
    ##Migration
    if (np.mod(t,beta*N)==0):
        for p in range(Ng):
            sample[p]=rd.sample(subset[p][0]+subset[p][1],lim)
            for l1 in sample[p]:
                agents[l1][5]=int(abs(agents[l1][5]-1))##so pra dous grupos
                agents[l1][6]+=1
        for k in range(Ng):
            for j in range(2):
                subset[k][j]=[i for i in range(N) if (agents[i][1]==j and agents[i][5]==k)]    
        stimula=[[0]*num for i in range(Ng)]
for i in range(N):
    if (prob[i][2]<cutoff):prob[i][2]=0.0
    if (prob[i][2]>(1.0-cutoff)):prob[i][2]=1.0

print(time.time()-start)
del stimulatemp[0]
for j in range(Ng):
    plt.plot([stimulatemp[i][j] for i in range(len(stimulatemp))])