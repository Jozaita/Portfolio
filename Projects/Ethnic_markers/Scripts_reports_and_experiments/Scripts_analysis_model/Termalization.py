##Imports
import random as rd
import numpy as np
import time
import math
from matplotlib import pyplot as plt
from scipy import stats
##Simulation variables
start=time.time()
N=1000
T=400*N
sim=1
delta=0.5
delta1=0
h1=0
e=0.5
h=0
l=0.5
pdif=4 #number of different probabilities (2xbehaviours)
A=np.zeros([2,2])   #Payoff matrix
A[0,0]=1+delta+delta1
A[0,1]=1-h1
A[1,0]=1
A[1,1]=1+delta
##Agents variables
agents=[[0]*5 for i in range(N)] ##(beh,mar,pay,int,asp)
prob=[[0]*pdif for i in range(N)]##(p=a,p=b,p!a,p!b)
stim=[0]*2
action=[0]*2
a=[0]*2
bins=np.linspace(0,1,50)
heat=np.zeros((len(bins)-1,len(bins)-1))
aspirations=[0.8,0.8,0.8,1.1]
uasp=list(np.unique(aspirations))
num=int(math.factorial(len(uasp)+1)/(math.factorial(len(uasp)-1)*2))
term=0


##Functions
def interact(a,b):
    a[3]+=1
    b[3]+=1
    if(a[0]==b[0]):
        a[2]+=1
        b[2]+=1
    
    return
def norm(prob,action):
    if (np.mod(action,2)==0):
        action2=action+1
    else:
        action2=action-1
    prob[action2]=1.0-prob[action]
    return
for s in range(sim):
    ##Initial conditions
    stimula=[0]*num
    stimulatemp=[[0]*num for i in range(T//N)]
    for i in range(N):
        agents[i][0]=rd.randint(0,1)
        agents[i][1]=rd.randint(0,1)
        agents[i][2]=0
        agents[i][4]=rd.choice(aspirations)
        agents[i][3]=0
        for j in range(pdif):
            if (np.mod(j,2)==0):
                prob[i][j]=rd.uniform(0,1)
            else:
                prob[i][j]=1-prob[i][j-1]
    subset=[0]*2
    for j in range(2):
        subset[j]=[i for i in range(N) if agents[i][1]==j]
    
    ##Dynamics
    for t in range(T):
        ##Termalization
        if (t==(200*N)):
            for i in range(N):
                agents[i][2]=0
                agents[i][3]=0
        ##Parameter e
        a11=rd.uniform(0,1)
        if (a11>e): ##Marker interaction, choose field of action
            ##Choose couple
            b=rd.randint(0,1)
            couple=rd.sample(subset[b],2)
            ##Choose field of action
            for i in range(2):
                a[i]=rd.uniform(0,1)
                action[i]=prob[couple[i]][0]
                kaux=0
        else: ## Non-marker interaction
            ##Choose couple
            couple=rd.sample(range(N),2)
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
        stimula[uasp.index(agents[couple[0]][-1])+uasp.index(agents[couple[1]][-1])]+=1-stim.index(round(abs(stimulus*max(stim)),4))
            #print(stim.index(round(abs(stimulus*max(stim)),4)),uasp.index(agents[i][4]))
            #print(agents[i])
        if ((np.mod(t,N)==0) and t>0):
            #for j in range(num):
                #for i in range(2):
                    #stimula[j][i]=stimula[j][i]/(2*N)
                    for j4 in range(num):
                        #if (j4)==1:###Só valido pra isto
                        #    stimulatemp[t//N][j4]=stimula[j4]/2     
                        stimulatemp[t//N][j4]=stimula[j4]
                        #print(stimulatemp)
                    #print(int(t/N),stimulatemp[int(t/N)])
                    stimula=[[0]*num for i in range(Ng)]
    #if (stimulatemp[-1][0]==1.0):
    #    term+=1/sim 
    print(time.time()-start)
del stimulatemp[0]
###Normalization
#for i in range(len(stimulatemp)):
#    stimulatemp[i][1]/=2

####
if (sim==1):
    for i in range(num):
            plt.plot([stimulatemp[k1][i] for k1 in range(len(stimulatemp))],label=str(i))
    plt.legend()
    plt.show()
print(term)

