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
tfinal=5
a=2
d=0.05
deltat=0.001
simulations=arange(0,1000)
tpasos=tfinal/deltat
tiempo=linspace(0,tfinal,tpasos)
xdet=zeros(len(tiempo))
averx=zeros(len(tiempo))
averx2=zeros(len(tiempo))
averx4=zeros(len(tiempo))
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

for p in arange(0,int(tpasos-1)):
    for q in simulations: 
        averx[p]=averx[p]+matrix[p,q]
        averx2[p]=averx2[p]+matrix[p,q]*matrix[p,q]
        averx4[p]=averx4[p]+matrix[p,q]**4
    averx[p]=averx[p]/(simulations[-1]+1)
    averx2[p]=averx2[p]/(simulations[-1]+1)
    averx4[p]=averx4[p]/(simulations[-1]+1)
erroro1=averx2[int(1/deltat)]-averx[int(1/deltat)]*averx[int(1/deltat)]
erroro2=averx4[int(1/deltat)]-averx2[int(1/deltat)]*averx2[int(1/deltat)]
o1=averx[int(1/deltat)]
o2=averx2[int(1/deltat)]
o1_1.append(o1)
o2_1.append(o2)
error1.append(erroro1)
error2.append(erroro2)