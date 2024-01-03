# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 18:51:01 2017

@author: user
"""

#!python
from numpy import *
import pylab as p
from scipy import integrate 
from matplotlib import pyplot as plb 
from matplotlib import animation
# Definition of parameters
s= 15
a = 240
c = 25
inicio=0
fin=1
pasos=1000
muestra=zeros((pasos,pasos,1))
Y=zeros(2)
f=zeros(pasos)
g=zeros(pasos)
def dX_dt(X, t=0):
#""" Definimos la ecuacion . """
    return array([a-c*X[0]-4*X[0]*X[1]/(1+X[0]**2),
                  s*(c*X[0]-X[0]*X[1]/(1+X[0]**2))])
dimu=linspace(inicio,fin,pasos)
dimv=linspace(inicio,fin,pasos)
contadoru=-1
contadorv=-1
for Y[0] in dimu :
 contadoru=contadoru+1
 contadorv=0
 for Y[1] in dimv:
  Y[0]=dimu [contadoru] 
  Y[1]=dimv[contadorv]
  solucion=dX_dt(Y,t=0)
  f[contadoru]=solucion[0]
  g[contadoru]=solucion[1]
f1=p.figure()
p.plot(dimu,f,label='f(u)')
p.plot(dimu,g,label='g(u)')
p.grid()
p.legend(loc='best')
