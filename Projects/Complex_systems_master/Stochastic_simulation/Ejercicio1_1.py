x# -*- coding: utf-8 -*-
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
tfinal=3
a=2
d=0.05
deltat=0.01
simulations=arange(0,10)
tpasos=tfinal/deltat
tiempo=linspace(0,tfinal,tpasos)
xdet=zeros(len(tiempo))
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
f1=p.figure(figsize=(10,8))
plb.plot(tiempo,xdet,'black',linewidth=2)
for i in simulations:
 plb.plot(tiempo,matrix[:,i],alpha=0.5)
f1.savefig('Fig1_1.png')