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
s= 1
a = 5
c = 10
inicio=0
fin=1
pasos=1000
muestra=zeros((pasos,pasos,1))
Y=zeros(2)
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
  if solucion[0]>0 and solucion[1]>0:
   muestra [contadoru,contadorv,0]=3
  if solucion[0]>0 and solucion[1]<0:
   muestra[contadoru,contadorv,0]=2
  if solucion[0]<0 and solucion[1]>0:
   muestra[contadoru,contadorv,0]=1
  if solucion[0]<0 and solucion[1]<0:
   muestra[contadoru,contadorv,0]=0
  contadorv=contadorv+1
fig,ax= p.subplots(figsize=(6,6))
cax=ax.imshow(muestra[:,:,0],cmap=p.cm.coolwarm, interpolation='none', extent=[inicio,fin,inicio,fin])
cbar = fig.colorbar(cax, ticks=[3,2 , 1,0], orientation='horizontal')
cbar.ax.set_xticklabels(['3','2','1','0'])  # horizontal colorbar
c='Valor c ='+str(round(i*(fin-inicio)/pasos+inicio,2))