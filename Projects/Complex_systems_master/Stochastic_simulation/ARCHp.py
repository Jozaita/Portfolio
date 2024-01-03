import numpy as np
import random as rd
from matplotlib import pyplot as plb
import time
start=time.time()
p=1
q=1
tfinal=10**5
alpha=[0]*(p+1)
beta=[0]*(q+1)
s=[0]*(tfinal)
x=[0]*(tfinal)
sigma=[0]*(tfinal)
#Define all p-dependent parameters
alpha[0]=0.5
alpha[1]=0.5

#Entering parameters
for t in range(0,tfinal):
    sigma[t]=alpha[0]    
    for j in range(1,p+1):    
        sigma[t]=sigma[t]+alpha[j]*x[t-j]**2+beta[j]*sigma[t-j]**2    
    x[t]=np.sqrt(sigma[t])*rd.gauss(0,1)
    s[t]=sum(x)

lenx=len(x)
m1=0
m2=0
m4=0
x1=[0]*tfinal
logp=[0]*tfinal
for i in range(0,lenx):
 m1=m1+x[i]
 m2=m2+x[i]*x[i]
 m4=m4+x[i]**4
 x1[i]=abs(x[i])
 logp[i]=np.log(x[i])
m1=m1/lenx
m2=m2/lenx
m4=m4/lenx
c=m4/(m2**2)-3
f1=plb.figure(0)
plb.plot(s)


hist1=np.histogram(x1,bins=100,range=(min(x1),max(x1)),normed=1)
f1=plb.figure()
ax=plb.gca()
plb.loglog(hist1[1][:-1],hist1[0],'o')

hist2=np.histogram(x,bins=100,normed=1)
f2=plb.figure()
ax=plb.gca()
plb.plot(hist2[1][:-1],hist2[0],'o')
print(time.time()-start)