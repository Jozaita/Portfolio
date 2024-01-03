# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 18:43:00 2017

@author: user
"""

#ok , so we consider the general case I as the noise is not a function of x. 
from numpy import *
import numpy as np
import pylab as p
import matplotlib
from scipy import integrate 
from matplotlib import pyplot as plb
tfinal=500
a=2
d=0.05
deltat=0.01
tpasos=tfinal/deltat
tiempo=arange(0,tfinal,deltat)
s1=arange(0,10,10*deltat)
corr1=zeros(len(s1))
xini=0
xfinal=zeros(int(tfinal/0.1))
xfinal[0]=0
n=1
while n<tpasos-1:
  u=random.normal()
  xini=xini+deltat*(-a*xini)+sqrt(deltat)*u
  if mod(n,10)==0:
         xfinal[int(n/10)]=xini
  n=n+1
  print(n)

for i in arange(0,len(xfinal)):
     xfinal[i]=xfinal[i]*sqrt(d)
for s in arange(0,len(corr1)):
 for p in arange(0,len(xfinal)-s):
    corr1[s]=corr1[s]+xfinal[p]*xfinal[p+s]
 corr1[s]=corr1[s]/(len(xfinal-s))
f1=plb.figure()
l2,=plb.plot(s1,corr1)
l1,=plb.plot(arange(0,10,deltat),corr)
plb.legend([l2,l1],['Average on time','Average on simulations t=5'])
f1.savefig('Fig1_5.png')