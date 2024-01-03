# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:13:26 2017

@author: user
"""

from numpy import *
import numpy as np
import pylab as p
import matplotlib
from scipy.special import erfinv 
from matplotlib import pyplot as plb
M=10**6
n=0
exitos=[]
x=zeros(50)
f=zeros(50)
for i in arange(0,M):
 u=random.uniform()
 v=random.uniform()
 z=sqrt(2)*erfinv(2*u-1)
 if v<exp(+z**2-z**4-1/4):
    exitos.append(z)
    n=n+1
x=linspace(min(exitos),max(exitos),50)
p=n/M
f1=plb.figure()
n,bins,_=plb.hist(exitos,bins=100,normed=1)
mid = 0.5*(bins[1:] + bins[:-1])
plb.errorbar(mid, n, yerr=sqrt(p*(1-p)/M), fmt='none',elinewidth=3,ecolor='black')
c=exp(-1/4)/(sqrt(2*pi)*p)
plb.plot(x,c*exp(0.5*x**2-x**4),color='r',linewidth=2)
plb.xlim([min(exitos),max(exitos)])
plb.ylim([0,max(n)])
errc=sqrt(p*(1-p)/(M*2*pi))*p**(-2)*exp(0.25)
print('El valor de la constante es', c )
print('El error de la constate es',errc)
f1.savefig('Ejercicio51.png')


