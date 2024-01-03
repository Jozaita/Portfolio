
import numpy as np 
import networkx as nx
import random as rd
import time
import sys
from matplotlib import pyplot as plb
corr=[0]*100
corr2=[0]*100
retsim=[0]*int(len(ret)/100)
tsim=[]
for j in range(0,len(ret)):
    if np.mod(j,100)==0:
     retsim[int(j/100)]=ret[j]
     tsim.append(j)
mediaret=np.average(ret)
varret=np.sqrt(np.var(ret))
normret=[0]*len(ret)
for i in range(0,len(ret)):
    normret[i]=(ret[i]-mediaret)/varret
    
for s in range(0,100):
 
 for p in range(0,len(ret)-100):
      
      corr[s]=corr[s]+ret[p]*ret[p+s]
      corr2[s]=corr2[s]+ret[p]**2*ret[p+s]**2
 corr[s]/=corr[0]
 corr2[s]/=corr2[0]
f4=plb.figure()
plb.plot(range(0,100),corr,linestyle='--',label='Correlation x')
plb.plot(range(0,100),corr2,linestyle='--',label='Correlation x^2') 
plb.title('Correlations',fontsize=16)
plb.xlabel('time',fontsize=16)
plb.ylabel('Correlation',fontsize=16)
plb.legend()
f4.savefig('Correlations.jpg')

f5=plb.figure()
plb.plot(range(0,len(pre)),pre,label='Price')
plb.title('Price',fontsize=16)
plb.xlabel('time',fontsize=16)
plb.ylabel('Price',fontsize=16)
plb.legend()
f5.savefig('Price.jpg') 

f6=plb.figure()
plb.plot(tsim,retsim,label='Return') 
plb.title('Return',fontsize=16)
plb.xlabel('time',fontsize=16)
plb.ylabel('Return',fontsize=16)
plb.legend()
f6.savefig('Return.jpg')    

    


hist5=np.histogram(normret,bins=100)
hist6=np.histogram(normret[-100:],bins=100)
f1=plb.figure()
#plb.xlim((-100, 100))
plb.semilogy(hist5[1][:-1],hist5[0],'o')
plb.semilogy(hist6[1][:-1],hist6[0],'o')