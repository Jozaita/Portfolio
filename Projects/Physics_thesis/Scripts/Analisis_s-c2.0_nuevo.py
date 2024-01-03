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
#Borramos lo creado 


# Definition of parameters
contadorc=0
contadors=0
pasos=1000
rango=linspace(0.01,60,pasos)
rango2=linspace(0.01 ,60,pasos)
linea=linspace(15,15,pasos)
x1=[]
y1=[]
y2=[]
y3=[]
y4=[]
taus=[]
omegasr=[]
omegasc=[]
a=240
cray=zeros((pasos,pasos,1))
for s in rango:
 contadors=0
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
  x1.append(s)
  y1.append(lambda1.imag)
  y2.append(lambda1.real)
  y3.append(lambda2.imag)
  y4.append(lambda2.real)
  tau=lambda1+lambda2
  delta=lambda1*lambda2
  alpha=tau/2
  omega=csqrt(4*delta-tau**2)/2
  separacion=tau**2-4*delta
  taus.append(tau)
  omegasr.append(omega.real)
  omegasc.append(omega.imag)
# Intentemos dibujar un mapa de bifurcaciones asignando un color en funcion del 
#tipo de variable 
  if delta>0:
   if tau>0 :
    if separacion>0:
     cray[contadorc,contadors,0]=5 #Nodos inestables
    if separacion<0:
     cray[contadorc,contadors,0]=4 #Espirales inestables
   if tau<0 :
    if separacion>0:
     cray[contadorc,contadors,0]=3 #Nodos estables
    if separacion<0:
     cray[contadorc,contadors,0]=2 #Espirales estables
  if delta<0:
    cray[contadorc,contadors,0]=1 #Punto de silla
  contadors=contadors+1
 contadorc=contadorc+1
f1=p.figure(0,figsize=(10,8))
p.pcolormesh(rango2,rango,cray[:,:,0],cmap='gnuplot')
p.plot(rango,linea,'c--',linewidth=3)
p.annotate('Zona de interes', xy=(20, 15), xytext=(5, 25),size=20,
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
p.title('Plano s-c')
p.colorbar()
f1.savefig('Plano c-s')





