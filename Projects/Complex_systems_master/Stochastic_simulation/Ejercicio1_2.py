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
deltat=0.01
simulations=arange(0,1000 )
tpasos=tfinal/deltat
tiempo=linspace(0,tfinal,tpasos)
xdet=zeros(len(tiempo))
averx=zeros(len(tiempo))
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

for p in arange(0,int(tpasos-1)):
    for q in simulations: 
        averx[p]=averx[p]+matrix[p,q]
        averx2[p]=averx2[p]+matrix[p,q]*matrix[p,q]
    averx[p]=averx[p]/(simulations[-1]+1)   
    averx2[p]=averx2[p]/(simulations[-1]+1)
f1=plb.figure()
l1,=plb.plot(tiempo,averx,label='average x')
l2,=plb.plot(tiempo,averx2,label='average x^2')
plb.legend([l1,l2],['Average x','Average x^2'])
plb.legend()
f1.savefig('Fig1_2_3.png')