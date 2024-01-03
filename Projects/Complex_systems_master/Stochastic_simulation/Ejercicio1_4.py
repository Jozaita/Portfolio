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
tfinal=20
a=2
d=0.05
deltat=0.01
simulations=arange(0,1000)
tpasos=tfinal/deltat
tiempo=arange(0,tfinal,deltat)
s1=arange(0,10,deltat)
xdet=zeros(len(tiempo))
averx=zeros(len(tiempo))
corr=zeros(len(s1))
averx2=zeros(len(tiempo))
matrix=zeros([len(tiempo),len(simulations)])
matrix[0,:]=1/sqrt(d)
xdet[0]=1
for m in simulations:
 n=0
 while n<tpasos-1:
  
  u=random.normal()
  matrix[n+1,m]=matrix[n,m]+deltat*(-a*matrix[n,m])+sqrt(deltat)*u
  n=n+1
  print(m,n)

for i in arange(0,len(tiempo)):
 for j in arange(0,len(simulations)):
     matrix[i,j]=matrix[i,j]*sqrt(d)
n=0
while n<tpasos-1:
 xdet[n+1]=xdet[n]-deltat*(a*xdet[n])
 n=n+1
#%%
f1=plb.figure()
for p in [50,100,200,500]:
 for s in arange(0,len(corr)):

    for q in simulations: 
      corr[s]=corr[s]+matrix[p,q]*matrix[p+s,q]
    corr[s]=corr[s]/(simulations[-1]+1)
 l2,=plb.plot(s1,corr,label='t='+str(int(p*deltat)))
 plb.legend([l2],['t='+str(int(p*deltat))])
f1.savefig('Fig1_4.png')
