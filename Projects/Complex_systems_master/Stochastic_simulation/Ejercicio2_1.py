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
a=4
b=1
d=0.01
deltat=0.01
simulations=arange(0,21)
tpasos=tfinal/deltat
tiempo=linspace(0,tfinal,tpasos)
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
f1=p.figure()
plb.plot(tiempo,xdet,'black',linewidth=2)
for i in simulations:
 plb.plot(tiempo,matrix[:,i],alpha=0.5)
f1.savefig('Fig2_1.png')