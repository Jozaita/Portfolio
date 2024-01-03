#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 13:34:45 2017

@author: jozaita
"""
import numpy as np
import random
from matplotlib import pyplot as plb
trayec=1000
tiempo=100
a_2=2
d=0.05
h=0.01
s1=np.arange(0,10,h)
corr=np.zeros(len(s1))
tau2=[0.5,0.05,0.005]
num=int(tiempo/h)
matrix=np.zeros([num,trayec])
matrix[0,:]=1
f1=plb.figure()
for tau in tau2:
 for i in range(0,trayec):
  hor=[]
  ver=[]
  p=np.exp(-h/tau)
  b=-np.sqrt(tau/2)*(1-p)*random.gauss(0,1)
  gh=0
  a=0
  x=1
  alpha=np.sqrt(h)
  beta=-tau*(1-p)/np.sqrt(h)
  gamma=np.sqrt(tau*(1-p*p)/2-tau*tau*(1-p)*(1-p)/h)
  for t in range(1,num):
   a_old=a
   b_old=b
   def q(x):
      return -a_2*x
 #Generation of gh
   u=random.gauss(0,1)
   v=random.gauss(0,1)
   a=alpha*u
   b=beta*u+gamma*v
   gh=p*gh-p*a_old+a-b_old+b
   aux=h*q(x)+gh*np.sqrt(d)
   x=x+0.5*(aux+h*q(x+aux)+gh*np.sqrt(d))
   matrix[t,i]=x
 
 for p in [50]:
  for s in np.arange(0,len(corr)):

    for q in range(0,trayec): 
      corr[s]=corr[s]+matrix[p,q]*matrix[p+s,q]
    corr[s]=corr[s]/(trayec)
 l2,=plb.plot(s1,corr,label='t='+str(int(p*h)))   
 plb.legend([l2],['tau='+str(tau)])
 plb.xlim(0,max(s1))
 plb.title('Correlation, t='+str(p*h))
f1.savefig('Corr_t='+str(p*h)+'.png')