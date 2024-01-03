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
pasos=1000
s=1
contador=1
rango=linspace(-1,100,pasos)
x1=[]
y1=[]
y2=[]
y3=[]
y4=[]
cray=zeros((pasos+1,2))
for c in rango:
 contador=contador+1
 s = 1
 a = 1
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
 cray[contador-1,0]=c
 x1.append(c)
 y1.append(lambda1.imag)
 y2.append(lambda1.real)
 y3.append(lambda2.imag)
 y4.append(lambda2.real)
#Intentemos dibujar un mapa de bifurcaciones asignando un color en funcion del 
#tipo de variable 
 if type(lambda1)==float64 or type(lambda2)==float64:
  cray[contador-1,1]=1
 if type(lambda1)==complex128 or type(lambda2)==complex128:
  cray[contador-1,1]=-1



f1=p.figure(0)
p.plot(x1,y1, 'r-', label='Lambda1 Imaginario')
p.plot(x1,y2,'b', label='Lambda1 Real')
p.plot(x1,y3,'g',label='Lambda2 Imaginario')
p.plot(x1,y4,'c',label='Lambda2 Real')
p.grid()
p.legend(loc='best')
p.xlabel('Sigma')
p.title('Todas')
#Aislamos solo las complejas para estudiar la bifurcaciones Hopf
f2=p.figure(1)
p.plot(x1,y1, 'r-', label='Lambda1 Imaginario')
p.plot(x1,y3,'g',label='Lambda2 Imaginario')
p.grid()
p.legend(loc='best')
p.xlabel('Sigma')
p.title('Complejas')

