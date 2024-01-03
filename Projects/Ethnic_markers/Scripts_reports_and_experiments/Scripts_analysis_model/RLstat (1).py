##Imports
import random as rd
import numpy as np
import time
import math
from matplotlib import pyplot as plt
from scipy import stats
##Simulation variables
start=time.time()
N=500
T=10**5
sim=100
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
aspirations=[0.8,1.1,1.5]
uasp=list(np.unique(aspirations))
##Correlation and CI vector 
corrvec=[[0,0] for i in range(len(uasp)+1)]
corrfactor=[[0,0] for i in range(len(uasp)+1)]
civec=[[0]*100 for i in range(len(uasp)+1)]
heat=[np.zeros((len(bins)-1,len(bins)-1)) for i in range(len(uasp)+1)]
####Cutoff for pearsonR
cutoff=10**(-2)
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
    for i in range(N):
        agents[i][0]=rd.randint(0,1)
        agents[i][1]=rd.randint(0,1)
        agents[i][2]=0
        agents[i][3]=0
        agents[i][4]=rd.choice(aspirations)
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
                stim[j]=abs(A[j,0]-agents[i][4])
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
    for i in range(N):
        if (prob[i][2]<cutoff):prob[i][2]=0.0
        if (prob[i][2]>(1.0-cutoff)):prob[i][2]=1.0    
    k3=-1
    for j in uasp:
        k3+=1
        heat[k3]+=np.histogram2d([prob[i][0] for i in range(N) if agents[i][4]==j],\
                                 [prob[i][2] for i in range(N) if agents[i][4]==j],\
                                 bins=bins,normed=True)[0]
        civec[k3]+=np.histogram([agents[i][2]/agents[i][3] for i in range(N) if agents[i][4]==j],bins=100,range=(0,1))[0]
        k4=-1
        for u in [0,2]:
            k4+=1
            pearson=stats.pearsonr([agents[i][1] for i in range(N) if agents[i][4]==j],\
                                                       [prob[i][u] for i in range(N) if agents[i][4]==j])[0]
            if (math.isnan(pearson)==False): 
                corrvec[k3][k4]+=np.arctanh(abs(pearson))
                corrfactor[k3][k4]+=1
    civec[-1]+=np.histogram([agents[i][2]/agents[i][3] for i in range(N)],bins=100,range=(0,1))[0]
    heat[-1]+=np.histogram2d([prob[i][0] for i in range(N)],\
                             [prob[i][2] for i in range(N)],\
                             bins=bins,normed=True)[0]
    k4=-1
    for u in [0,2]:
        k4+=1
        pearson=stats.pearsonr([agents[i][1] for i in range(N)],\
                                                   [prob[i][u] for i in range(N)])[0]
        if (math.isnan(pearson)==False):
            corrvec[-1][k4]+=np.arctanh(abs(pearson))
            corrfactor[-1][k4]+=1

    print(s)
for i in range(len(uasp)+1):
    for j in range(2):
        if (corrfactor[i][j]>0):
            corrvec[i][j]=corrvec[i][j]/corrfactor[i][j]
for i in range(len(uasp)+1):
    for j in range(2):
        corrvec[i][j]=np.tanh(corrvec[i][j])

    #print([agents[i][1] for i in range(N)].count(0))
    #print([agents[i][1] for i in range(N)].count(1))

#plt.hist([prob[i][0] for i in range(N)],bins,alpha=0.5, label='=,a',normed=True)
#plt.hist([prob[i][1] for i in range(N)],bins,alpha=0.5, label='=,b',normed=True)
#plt.hist([prob[i][2] for i in range(N)],bins,alpha=0.5, label='!,a',normed=True)
#plt.hist([prob[i][3] for i in range(N)],bins,alpha=0.5, label='!,b',normed=True)
#fig, axs = plt.subplots(2, 1)
#fig.tight_layout(pad=2.0)
#axs[0].hist([prob[i][0] for i in range(N)],bins,label='=',density=True)
#axs[0].title.set_text('=,0')
#axs[1,0].hist([prob[i][1] for i in range(N)],bins,label='0',density=True)
#axs[1,0].title.set_text('=,1')
#axs[1].hist([prob[i][2] for i in range(N)],bins,label='!',density=True)
#axs[1].title.set_text('!,0')
#axs[1,1].hist([prob[i][3] for i in range(N)],bins,label='1',density=True)
#axs[1,1].title.set_text('!,1')
#plt.xlabel('!,0')
#plt.ylabel('=,0')
#plt.imshow(heat,extent=[1,0,0,1])
#plt.colorbar()