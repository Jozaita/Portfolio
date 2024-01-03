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
d1=0
rango=arange(0.01,1,0.01)
averagetim=zeros(len(rango))
vartim=zeros(len(rango))
f1,ax=plb.subplots()
rango=arange(0.01,1,0.01)
for d in rango:
 print(d)

 xdet=zeros(len(tiempo))
 inttime=[]
 matrix=zeros([len(tiempo),len(simulations)])
 matrix[0,:]=0
 xdet[0]=0

 for m in simulations:
  n=0
  while n<tpasos-1:

   u=random.normal()
   matrix[n+1,m]=matrix[n,m]+deltat*(a*matrix[n,m]-b*matrix[n,m]**3)+sqrt(deltat*d)*u
   n=n+1
   
#%%

 i=0
 j=0
 while j<len(simulations)-1:
  if abs(matrix[i,j])>0.5:
             inttime.append(i*deltat)
             j=j+1
             i=0
  i=i+1
 plb.hist(inttime,bins=100,normed=1)
 plb.title('First passage time histogram for d=0.01')
 histo=histogram(inttime,bins=100)
 histo= [histo[0], 0.5*(histo[1][1:]+histo[1][:-1])]
 averagetim[d1]=sum(histo[0]*histo[1])/len(inttime)
# ax.plot(histo[0])

 for i in arange(0,len(histo[1])-1):
  vartim[d1]=vartim[d1]+1/(len(inttime)-1)*(histo[1][i]**2-averagetim[d1]**2)
 d1=d1+1
#%%
f2=p.figure()
plb.plot(rango,averagetim)
plb.title('Average first passage time')
f2.savefig('Fig2_4_1.png')
f3=p.figure()
plb.plot(rango,vartim)
plb.title('Variance first passage time')
f3.savefig('Fig2_4_2.png')
#f1.savefig('Fig2_4_3')