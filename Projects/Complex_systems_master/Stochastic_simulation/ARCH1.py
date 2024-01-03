import numpy as np
import random as rd
from matplotlib import pyplot as plb
import time
start=time.time()
a_0=0.5
a_1=0.5
p=1
alpha=[0]*(p+1)
x=[0]*(p+1)
#Define all p-dependent parameters
alpha[0]=0.5
alpha[1]=0.5

p=[]
#Entering parameters
for t in tprep:
    for j in range(0,p)
    x[t]=alpha[t]*rd.gauss(0,1)
x.append(rd.gauss(0,1)*a_0)
t=0
tfinal=2*10**4
while (t<tfinal):
 s=a_0+a_1*x[t]**2
 g=rd.gauss(0,1)
 x.append(np.sqrt(s)*g)
 p.append(sum(x))
 t=t+1
lenx=len(x)
m1=0
m2=0
m4=0
c=0
for i in range(0,lenx):
 m1=m1+x[i]
 m2=m2+x[i]*x[i]
 m4=m4+x[i]**4
m1=m1/lenx
m2=m2/lenx
m4=m4/lenx
c=m4/(m2**2)-3
f1=plb.figure(0)
plb.plot(x)
f2=plb.figure(1)
plb.plot(p)
f3=plb.figure(2)
plb.plot(np.log(p))
time=time.time()-start
