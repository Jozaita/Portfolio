
from numpy import *
import numpy as np
import pylab as p
import matplotlib
from scipy.special import gamma
from scipy.special import erfinv 
from matplotlib import pyplot as plb
alpha=0.5
M=10**6
n=0

exitos=[]
for i in arange(0,M):
 u=random.uniform()
 v=random.uniform()
 p1=(e+alpha)/e
 p=p1*u
 if p<1:
     x=p**(1/alpha)
     if v<exp(-x):
         exitos.append(x)
         n=n+1
 if p>=1:
     x=-log((p1-p)/alpha)
     if v<x**(alpha-1):
         exitos.append(x)
         n=n+1
p=n/M
y=linspace(0,max(exitos),500)
f1=plb.figure()
n,bins,_=plb.hist(exitos,bins=100,normed=1)
mid = 0.5*(bins[1:] + bins[:-1])
plb.errorbar(mid, n, yerr=sqrt(p*(1-p)/M), fmt='none',elinewidth=3,ecolor='black')
plb.plot(y,exp(-y)*y**(alpha-1)/gamma(alpha),color='r',linewidth=2)
plb.xlim([0,max(exitos)])
plb.ylim([0,max(n)])
f1.savefig('Ejercicio48.png')
