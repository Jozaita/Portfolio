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
T=2*10**5
delta=0.5
delta1=0
h1=0
e=0.5
h=0
l=0.5
beta=0.01
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
agents=[[0]*6 for i in range(N)] ##(beh,mar,pay,int,asp,group)
prob=[[0]*pdif for i in range(N)]##(p=a,p=b,p!a,p!b)
stim=[0]*2
stimula=[0]*2
stimulatemp=[[0]*2 for i in range(int(T/N))]
action=[0]*2
a=[0]*2
aspirations=[1.1]
uasp=list(np.unique(aspirations))
sample=[0]*Ng
##Correlation and CI vector 
heat=[np.zeros((len(bins)-1,len(bins)-1)) for i in range(Ng+1)]
corrvec=[[0,0] for i in range(Ng+1)]
corrfactor=[[0,0] for i in range(Ng+1)]
civec=[[0]*100 for i in range(Ng+1)]
####Cutoff for pearsonR
cutoff=10**(-10)
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
    if (i<N/2):
            agents[i][5]=0
    else:
            agents[i][5]=1
    for j in range(pdif):
        if (np.mod(j,2)==0):
            prob[i][j]=rd.uniform(0,1)
        else:
            prob[i][j]=1-prob[i][j-1]
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
    ##Migration
    if (np.mod(t,beta*N)==0):
        for p in range(Ng):
            sample[p]=rd.sample(subset[p][0]+subset[p][1],lim)
            for l1 in sample[p]:
                agents[l1][5]=int(abs(agents[l1][5]-1))##so pra dous grupos
        for k in range(Ng):
            for j in range(2):
                subset[k][j]=[i for i in range(N) if (agents[i][1]==j and agents[i][5]==k)]    
for i in range(N):
    if (prob[i][2]<cutoff):prob[i][2]=0.0
    if (prob[i][2]>(1.0-cutoff)):prob[i][2]=1.0
k3=-1
for j in range(Ng):
        k3+=1
        heat[k3]+=np.histogram2d([prob[i][0] for i in range(N) if agents[i][5]==j],\
                                 [prob[i][2] for i in range(N) if agents[i][5]==j],\
                                 bins=bins,normed=True)[0]
        civec[k3]+=np.histogram([agents[i][2]/agents[i][3] for i in range(N) if agents[i][5]==j],bins=100,range=(0,1))[0]
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
            
for i in range(Ng+1):
    for j in range(2):
        if (corrfactor[i][j]>0):
            corrvec[i][j]=corrvec[i][j]/corrfactor[i][j]
for i in range(Ng+1):
    for j in range(2):
        corrvec[i][j]=np.tanh(corrvec[i][j])
#for i in range(len(uasp)):
#    for j in range(2):
#        corrvec[i][j]=corrvec[i][j]/corrfactor[i][j]
#for i in range(len(uasp)):
#    for j in range(2):
#        corrvec[i][j]=np.tanh(corrvec[i][j])
print(time.time()-start)
#print([agents[i][1] for i in range(N)].count(0))
#print([agents[i][1] for i in range(N)].count(1))
bins=np.linspace(0,1,50)
#plt.hist([prob[i][0] for i in range(N)],bins,alpha=0.5, label='=,a',normed=True)
#plt.hist([prob[i][1] for i in range(N)],bins,alpha=0.5, label='=,b',normed=True)
#plt.hist([prob[i][2] for i in range(N)],bins,alpha=0.5, label='!,a',normed=True)
#plt.hist([prob[i][3] for i in range(N)],bins,alpha=0.5, label='!,b',normed=True)
fig, axs = plt.subplots(2, 1) 
fig.tight_layout(pad=2.0)
axs[0].hist([prob[i][0] for i in range(N)],bins,label='=',density=True)
axs[0].title.set_text('=,0')
#axs[1,0].hist([prob[i][1] for i in range(N)],bins,label='0',density=True)
#axs[1,0].title.set_text('=,1')
axs[1].hist([prob[i][2] for i in range(N)],bins,label='!',density=True)
axs[1].title.set_text('!,0')
#axs[1,1].hist([prob[i][3] for i in range(N)],bins,label='1',density=True)
#axs[1,1].title.set_text('!,1')
plt.close()
for j in range(Ng):
    for j2 in range(2):
        fig3=plt.figure()
        plt.hist2d([prob[i][0] for i in range(N) if (agents[i][-1]==j and agents[i][1]==j2)],\
                    [prob[i][2] for i in range(N) if (agents[i][-1]==j and agents[i][1]==j2)],bins=bins,cmap='viridis')
        plt.xlabel('=,0')
        plt.ylabel('!=,0')
        plt.title(str(j)+','+str(j2))
        cb=plt.colorbar()
        plt.show()
        plt.close()
fig2=plt.figure()
plt.hist2d([prob[i][0] for i in range(N)],[prob[i][2] for i in range(N)],bins=bins,cmap='viridis')
plt.xlabel('=,0')
plt.ylabel('!=,0')
cb=plt.colorbar()


matrix=[np.zeros((Ng,Ng)) for i in range(Ng)]
coinc=[0,0]
for i in range(Ng):
    pointer=int(2*i)
    for j in range(Ng):
        for k in range(Ng):
            matrix[i][j,k]=round(np.mean([ prob[i][pointer] for i in range(N)\
                   if (agents[i][1]==k and agents[i][-1]==j)]),3)
for i2 in range(Ng):
    for j2 in range(Ng):    
        if (matrix[i2][0,j2]==matrix[i2][1,j2]):coinc[i2]+=1
for i in range(Ng):
    coinc[i]//=Ng    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

