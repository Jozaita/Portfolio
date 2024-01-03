# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 17:58:56 2016

@author: user
"""
#!python
from numpy import *
import pylab as p
import os
from numpy.lib.scimath import sqrt as csqrt
from matplotlib.colors import ListedColormap
#Borramos lo creado 


# Definition of parameters
contadors=0
contadora=0
contadorc=0
inicio=0.1
fin=60
inicio2=0.1
fin2=400
pasos=200
rango=linspace(inicio,fin,pasos)
rango2=linspace(inicio2,fin2,pasos)
x1=[]
y1=[]
y2=[]
y3=[]
y4=[]
cray=zeros((pasos,pasos,pasos,1))
for a in rango2:
 contadors=0
 for s in rango:
  contadorc=0
  for c in rango:
   def dX_dt(X, t=0):
  #""" Definimos la ecuacion . """
      return array([a-c*X[0]-4*X[0]*X[1]/(1+X[0]**2),
                    s*(c*X[0]-X[0]*X[1]/(1+X[0]**2))])
  #Colocamos los puntos fijos calculados 
   X_f0 = array([ a/(5*c), c*(1+(a/(5*c))**2)])
   zeros(2)==all(dX_dt(X_f0,t=0))  # => True                    !!!!!
  #Añadimos la jacobiana calculada para la matriz
   def d2X_dt2(X, t=0):
      #""" Matriz Jacobiana """
      return array([[-c-4*X[1]/(1+X[0]**2)*(1-2*X[0]**2/(1+X[0]**2)),   -4*X[0]/(1+X[0]**2)     ],
                    [s*(c-(X[1]/(1+X[0]**2)*(1-2*X[0]**2/(1+X[0]**2)))) ,   -s*X[0]/(1+X[0]**2)] ])
      #Esta matriz la tomamos para linealizar 
   A_f0=d2X_dt2(X_f0,t=0)
      #Llamamos a la funcion que calcula los autovalores
   lambda1, lambda2 = linalg.eigvals(A_f0)
 # Intentemos dibujar un mapa de bifurcaciones asignando un color en funcion del 
 #tipo de variable 
   tau=lambda1+lambda2
   delta=lambda1*lambda2
   alpha=tau/2
   omega=csqrt(4*delta-tau**2)/2
   separacion=tau**2-4*delta
   if delta>0:
    if tau>0 :
     if separacion>0:
      cray[contadora,contadors,contadorc,0]=5 #Nodos inestables
     if separacion<0:
      cray[contadora,contadors,contadorc,0]=4 #Espirales inestables
    if tau<0 :
     if separacion>0:
      cray[contadora,contadors,contadorc,0]=3 #Nodos estables
     if separacion<0:
      cray[contadora,contadors,contadorc,0]=2 #Espirales estables
   if delta<0:
      cray[contadora,contadors,contadorc,0]=1 #Punto de Silla
   contadorc=contadorc+1
  contadors=contadors+1
 contadora=contadora+1
 print(contadora)
i=0
while i <=pasos-1 : 
 fig,ax= p.subplots(figsize=(8,8)) 
 p.pcolormesh(rango,rango,cray[i,:,:,0],cmap='gnuplot')
 p.title('Plano c-s')
 p.colorbar()
 print(i)
 b='Valor a ='+str(round(i*(fin2-inicio2)/pasos+inicio2,2))
 p.savefig(str(b)+'.png')
 i=i+1
