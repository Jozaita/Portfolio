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
tfinal=10
a=4
b=1
d=0.01
deltat=0.01
simulations=arange(0,1000)
tpasos=tfinal/deltat
tiempo=linspace(0,tfinal,tpasos)
averx=zeros(len(tiempo))
averx2=zeros(len(tiempo))
averx4=zeros(len(tiempo))
varx2=zeros(len(tiempo))
xdet=zeros(len(tiempo))
matrix=zeros([len(tiempo),len(simulations)])
matrix[0,:]=0
xdet[0]=0
for m in simulations:
 n=0
 while n<tpasos-1:
  
  u=random.normal()
  matrix[n+1,m]=matrix[n,m]+deltat*(a*matrix[n,m]-b*matrix[n,m]**3)+sqrt(deltat*d)*u
  n=n+1
  print(m,n)


n=0
while n<tpasos-1:
 xdet[n+1]=xdet[n]+deltat*(a*xdet[n]-b*xdet[n]**3)
 n=n+1
for p in arange(0,int(tpasos-1)):
    for q in simulations: 
        averx[p]=averx[p]+matrix[p,q]
        averx2[p]=averx2[p]+matrix[p,q]*matrix[p,q]
        averx4[p]=averx4[p]+matrix[p,q]**4
    averx[p]=averx[p]/(simulations[-1]+1)
    averx2[p]=averx2[p]/(simulations[-1]+1)
    averx4[p]=averx4[p]/(simulations[-1]+1)
    varx2[p]=averx4[p]-averx2[p]*averx2[p]
#%%
f1=plb.figure()

l1,=plb.plot(tiempo,averx,label='average x')
l2,=plb.plot(tiempo,averx2,label='average x^2')
l3,=plb.plot(tiempo,averx2,label='average x^4')
l4,=plb.plot(tiempo,varx2,label='variance x^2')
plb.legend([l1,l2,l3,l4],['Average x','Average x^2','Average x^4','Variance x^2'])
plb.show(f1)
f1.savefig('Fig2_2.png')