##Imports
import random as rd
import numpy as np
import time
from matplotlib import pyplot as plt
##Simulation variables
start=time.time()
N=20
sim=100
T=10 
h=0
l=1
M=100
Qcheap=10
Qexp1=[20,40]
Qadd1=[10,50]
SpN=[0.25,0.5]
change2=[0]*(len(Qexp1)*len(Qadd1)*len(SpN))
finalres=[0]*(len(Qexp1)*len(Qadd1)*len(SpN))
finalres2=[0]*(len(Qexp1)*len(Qadd1)*len(SpN))
xres=[0]*(len(Qexp1)*len(Qadd1)*len(SpN))
heatmaps=[0]*(len(Qexp1)*len(Qadd1)*len(SpN))
aux4 = []
aux42 = []
nash=[10,20,6,12,20,20,8,16]
expres=[9.98,13.8,6.02,10.32,12.57,17.17,8.27,12.22]
bines=10
heat=np.zeros((bines,bines))
pdif=2 #number of different probabilities (2xbehaviours)
A=np.zeros((2,2))
fig,ax= plt.subplots(2,1,figsize=(12,9))
fig2,ax2=plt.subplots(2,4)
##Agents variables
k2=-1
n=1
n1=1
for Qexp in Qexp1:
    for Qadd in Qadd1:
        for s1 in SpN:
            prazas=int(N*s1)
            k2+=1
            A[0,0]=M-Qcheap
            A[0,1]=M-Qcheap-Qadd
            A[1,0]=M-Qexp
            A[1,1]=M-Qexp
            Aunique=np.unique(A)
            stim=[0]*len(Aunique)
            agents=[[0]*3 for i in range(N)] ##(payoff,aspiration,prob of choosing cheap)
            action=[0]*N
            atopo=[0]*N
            ncheap1=[0]*T
            ncheap2=[0]*T
            evol=[0]*(T+1)
            actionini=0
            actionini2=0
            for s in range(sim):
                change=[0]*N
                
                ##Initial conditions
                for i in range(N):
                    agents[i][0]=0
                    agents[i][1]=rd.gauss(A[1,1]-20,20)
                    agents[i][2]=s1*(1+(Qexp-Qadd-Qcheap)/M)
                    ##Normalize
                    if (agents[i][2]>1):agents[i][2]==1
                    if (agents[i][2]<0):agents[i][2]==0
                    #agents[i][2]=1##Initial probability of choosing cheap
                evol[0]=[agents[i][1] for i in range(N)]
                ##Dynamics
                for t in range(T):
                    atopo=[0]*N
                    ##All agents choose action according to probabilities
                    for i in range(N):
                         a1=rd.uniform(0,1)
                         ant=action[i]
                         if (a1<agents[i][2]):
                             ##Choose cheap
                             action[i]=0
                         else:
                             ##Choose expensive
                             action[i]=1
                         if (ant==action[i]):
                             change[i]+=1
                         else: 
                             change[i]=0
                    ncheap=action.count(0)
                    ncheap1[t]+=ncheap
                    ncheap2[t]+=ncheap**2
                    if (ncheap>prazas):
                        ##Choose at random the lucky ones
                        chosen=rd.sample([i for i in range(N) if action[i]==0],ncheap-prazas)
                        for i in chosen:
                            atopo[i]=1
                    ##For each agent:
                    for i in range(N):
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
                        if (action[i]==0):
                            if (stimulus>=0):
                                agents[i][2]+=(1-agents[i][2])*l*stimulus
                            else:
                                agents[i][2]+=agents[i][2]*l*stimulus
                        else:
                            if (stimulus>=0):
                                agents[i][2]*=(1-l*stimulus)
                            else:
                                agents[i][2]+=-(1-agents[i][2])*l*stimulus
                        ##Normalize
                        if (agents[i][2]>1):agents[i][2]==1
                        if (agents[i][2]<0):agents[i][2]==0
                    evol[t+1]=[agents[i][1] for i in range(N)]
                for i in range(N):
                    if ((change[i]>=5)and(action[i]==0)):
                        actionini+=1/N
                    if (change[i]>=5):
                        actionini2+=1/N
                heat=plt.hist2d([ agents[i][0] for i in range(N)],[agents[i][2] for i in range(N)],bins=bines,range=[[np.amin(A)*T,np.amax(A)*T],[0,1]])[0]
                heatmaps[k2]+=heat
            for i in range(T):    
                ncheap1[i]/=sim
                ncheap2[i]/=sim
                ncheap2[i]=np.sqrt(ncheap2[i]-ncheap1[i]**2)
            print(A)
            aux4.append(ncheap1)
            aux42.append(ncheap2)
            aux3=ax2[k2//4,round(np.mod(k2,4))]
            print(k2//4,round(np.mod(k2,4)))
            aux3.imshow(heatmaps[k2],extent=[0,1,np.amax(A)*T,np.amin(A)*T],aspect='auto')
            aux3.set_title(str(s1)+','+str(Qexp)+','+str(Qadd))
            actionini/=sim
            actionini2/=sim
            finalres[k2]=ncheap1[-1]
            finalres2[k2]=ncheap2[-1]
            xres[k2]=str(s1)+','+str(Qexp)+','+str(Qadd)
            ax[0].errorbar(range(T), ncheap1, yerr=ncheap2, fmt='-o',label=str(s1)+','+str(Qexp)+','+str(Qadd))
            ax[0].set_xlabel(r'Rounds')
            ax[0].set_ylabel(r'$\langle n_{cheap}\rangle _{sim}$')
            ax[0].legend()
#plt.savefig('Parking'+str(s1)+','+str(Qexp)+','+str(Qadd)+'.jpg')
print(actionini,actionini2)
ax[1].errorbar(xres,finalres,fmt='bo',yerr=finalres2,label='sim')
ax[1].errorbar(xres,nash,fmt='ro',label='nash')
ax[1].errorbar(xres,expres,fmt='go',label='experiment')
ax[1].legend()
ax[1].set_xlabel(r'S/N, $Q_{add}$,$Q_{exp}$')
ax[1].set_ylabel(r'$\langle n_{cheap}\rangle _{rounds,sim}$')
suma=0
for i in range(len(finalres)):
    suma+=abs(finalres[i]-expres[i])
    
print(suma)

fig.savefig('Parking.eps')
fig2.savefig('Parking2.eps')



f = open( 'variables.py', 'w' )
f.write('#Figure 1\n #X-axis\n')
f.write(str(list(range(T)))+'\n')
f.write('#Y-axis\n')
f.write('#Set up (parking ratio,competitors for cheap, y error)\n')
for i in range(len(list(zip(aux4,xres)))):
    f.write('\n')
    f.write(xres[i]+'#(parking spaces/size population,cost of expensive parking,penalty for not obtaining a space)'+'\n')
    f.write(str(aux4[i])+'\n')
    f.write(str(aux42[i])+'#Y-axis error \n')
f.write('\n #Figure 2\n #X-axis\n')
f.write(str(xres)+'\n')
f.write('#Figure 2\n #Y-axis\n')
f.write(str(finalres)+'\n')
f.write(str(finalres2)+'#Y-axis error \n')



f.close()