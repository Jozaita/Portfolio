##Imports
import random as rd
import numpy as np
import time
from matplotlib import pyplot as plt
##Simulation variables
start=time.time()
N=20
sim=100
T=20
h=0 
l=0.01
l2=l
M=100
cat=2
Qcheap=10
Qexp1=[20,40]
Qadd1=[10,50]
SpN=[0.25,0.5]
change2=[0]*(len(Qexp1)*len(Qadd1)*len(SpN))
finalres=[0]*(len(Qexp1)*len(Qadd1)*len(SpN))
finalres2=[0]*(len(Qexp1)*len(Qadd1)*len(SpN))
xres=[0]*(len(Qexp1)*len(Qadd1)*len(SpN))
nash=[10,20,6,12,20,20,8,16]
expres=[9.98,13.8,6.02,10.32,12.57,17.17,8.27,12.22]
pdif=2 #number of different probabilities (2xbehaviours)
A=np.zeros((2,2))
f1,ax=plt.subplots(2,1)

##Agents variables
k2=[0]*N
n=1
n1=1
k3=-1
#####Functions
def norm(prob,action):
    if (np.mod(action,2)==0):
        action2=action+1
    else:
        action2=action-1
    prob[action2]=1.0-prob[action]
    return
#####
for Qexp in Qexp1:
    for Qadd in Qadd1:
        for s1 in SpN:
            prazas=int(N*s1)
            k3+=1
            A[0,0]=M-Qcheap
            A[0,1]=M-Qcheap-Qadd
            A[1,0]=M-Qexp
            A[1,1]=M-Qexp
            Aunique=np.unique(A)
            stim=[0]*len(Aunique)
            agents=[[0]*3 for i in range(N)] ##(payoff,aspiration,occupation frequency detected by subject)
            prob=[[0]*2*cat for i in range(N)]
            action=[0]*N
            atopo=[0]*N
            ncheap1=[0]*T
            ncheap2=[0]*T
            #evol=[0]*(T+1)
            actionini=0
            actionini2=0
            for s in range(sim):
                change=[0]*N
                #MM=rd.choice([M,M-Qcheap-5,M-Qexp-5,M-Qcheap,M-Qexp])
                ##Initial conditions
                for i in range(N):
                    agents[i][1]=rd.uniform(np.amin(A),np.amax(A))
                    agents[i][2]=rd.uniform(0,1)
                #evol[0]=[agents[i][1] for i in range(N)]
                    for ij in range(2*cat-1):
                        prob[i][ij]=rd.uniform(0,1)
                    for ij in range(0,2*cat,2):
                         norm(prob[i],ij)
                ##Dynamics
                for t in range(T):
                    
                    atopo=[0]*N
                    ##All agents choose action according to frequency
                    for i in range(N):
                         
                         ant=action[i]
                         for i2 in range(cat):
                             if (agents[i][2]<=(1/cat)*(i2+1)): ##Categories for low occupation:
                                 k2[i]=i2*2
                                 break
                         a1=rd.uniform(0,1)
                                 #print(agents[i][2],(1/cat)*(i2+1))
                         if (a1<prob[i][k2[i]]):
                             action[i]=0 ##Escolhe barato
                         else:
                             action[i]=1
                         if (action[i]==ant):
                             change[i]+=1
                         else:
                             change[i]=0
                    ncheap=action.count(0)
                    if (ncheap>prazas):
                        ##Choose at random the lucky ones
                        chosen=rd.sample([i for i in range(N) if action[i]==0],prazas)
                        ##Chosen pra quedar
                        for i in chosen:
                            atopo[i]=1
                    ##For each agent:
                    for i in range(N):
                        ##Calculate frequency
                        if (action[i]==0):
                            if (atopo[i]==1):
                                laux=-1
                            elif (atopo[i]==0):
                                laux=1
                                action[i]=1
                            agents[i][2]+=laux*l2 
                            if (agents[i][2]>1): agents[i][2]=1
                            if (agents[i][2]<0): agents[i][2]=0
                    
                        ##Collect payofff
                        agents[i][0]+=A[action[i],atopo[i]]
                        currpay=A[action[i],atopo[i]]
                           
                        ##Calculate stimulus
                        for j in range(len(Aunique)):
                            stim[j]=abs(Aunique[j]-agents[i][1])
                        stimulus=(currpay-agents[i][1])/max(stim)
                        ##Update aspirations
                        agents[i][1]=(1-h)*agents[i][1]+h*currpay
                        ##Update probabilities
                        if (stimulus>=0):
                            prob[i][action[i]+k2[i]]+=(1-prob[i][action[i]+k2[i]])*l*stimulus
                        else:
                            prob[i][action[i]+k2[i]]+=prob[i][action[i]+k2[i]]*l*stimulus
                        norm(prob[i],action[i]+k2[i])
                    #ncheap=action.count(0)
                    ncheap1[t]+=ncheap
                    ncheap2[t]+=ncheap**2
                    #evol[t+1]=[agents[i][1] for i in range(N)]
                for i in range(N):
                    if ((change[i]>=5)and(action[i]==0)):
                        actionini+=1/N
                    if (change[i]>=5):
                        actionini2+=1/N
            
            for i in range(T):    
                ncheap1[i]/=sim
                ncheap2[i]/=sim
                ncheap2[i]=np.sqrt(ncheap2[i]-ncheap1[i]**2)
            actionini/=sim
            actionini2/=sim
            finalres[k3]=np.average(ncheap1)
            finalres2[k3]=np.average(ncheap2)
            xres[k3]=str(s1)+','+str(Qexp)+','+str(Qadd)
            ax[0].errorbar(range(T), ncheap1, yerr=ncheap2, fmt='-o',label=str(s1)+','+str(Qexp)+','+str(Qadd))
            #ax[0].title('Average people competing for cheap vs round') 
            #for i, txt in enumerate(ncheap1):
            #    ax.annotate(txt, (i, ncheap2[i]))
            plt.legend()
#plt.savefig('Parking'+str(s1)+','+str(Qexp)+','+str(Qadd)+'.jpg')
print(actionini,actionini2)
ax[1].errorbar(xres,finalres,fmt='bo',yerr=finalres2,label='sim')
ax[1].errorbar(xres,nash,fmt='ro',label='nash')
ax[1].errorbar(xres,expres,fmt='go',label='experiment')
plt.legend()
suma=0
for i in range(len(finalres)):
    suma+=abs(finalres[i]-expres[i])
    
print(suma)

#fig=plt.figure()
#plt.title('Evolution of aspirations')
#plt.xlabel('Round')
#plt.ylabel('Aspirations')
#for j in range(len(evol)):
#    plt.plot([evol[i][j] for i in range(T)])
#plt.plot([60 for i in range(T)],linewidth=3,label='Non-risky initial aspirations')
#plt.plot([90 for i in range(T)],linewidth=3,label='Risky initial aspirations')
#plt.legend()