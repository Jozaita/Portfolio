# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 17:58:56 2016

@author: user
"""
#!python
from numpy import *
import pylab as p
import os
#Borramos lo creado 


# Definition of parameters
contadors=0
contadora=0
a=0
pasos=1000
s=1
a=1
rango=linspace(0,1,pasos)
x1=[]
y1=[]
y2=[]
y3=[]
y4=[]
cray=zeros((pasos,pasos,1))
for s in rango:
 contadora=0
 for a in rango:
  c = 0.01
  def dX_dt(X, t=0):
 #""" Definimos la ecuacion . """
     return array([a-c*X[0]-4*X[0]*X[1]/(1+X[0]**2),
                   s*(c*X[0]-X[0]*X[1]/(1+X[0]**2))])
 #Colocamos los puntos fijos calculados 
  X_f0 = array([ a/(5*c), c*(1+(a/(5*c)**2))])
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
  x1.append(s)
  y1.append(lambda1.imag)
  y2.append(lambda1.real)
  y3.append(lambda2.imag)
  y4.append(lambda2.real)
# Intentemos dibujar un mapa de bifurcaciones asignando un color en funcion del 
#tipo de variable 
  if type(lambda1)==float64 or type(lambda2)==float64:
   if lambda1.real>0 and lambda2.real>0:
    cray[contadors,contadora,0]=5
   if lambda1.real*lambda2.real<0:
    cray[contadors,contadora,0]=4
   if lambda1.real<0 and lambda2.real<0:
    cray[contadors,contadora,0]=3
  if type(lambda1)==complex128 or type(lambda2)==complex128:
   if lambda1.real>0 and lambda2.real>0:
    cray[contadors,contadora,0]=2
   if lambda1.real*lambda2.real<0:
    cray[contadors,contadora,0]=1
   if lambda1.real<0 and lambda2.real<0:
    cray[contadors,contadora,0]=0
  contadora=contadora+1
 contadors=contadors+1
f1=p.figure()
p.pcolormesh(rango,rango,cray[:,:,0],cmap='gnuplot')
p.title('Plano s-a')
p.colorbar()






