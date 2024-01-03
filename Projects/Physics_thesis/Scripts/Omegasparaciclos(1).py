#!python
from numpy import *
import pylab as p
from scipy import integrate 
from matplotlib import pyplot as plb 
from matplotlib import animation
# Definition of parameters

s=  15
a = 240
c = 25
tini=0
tfin=60
tpasos=1001
t = linspace(tini, tfin   ,  tpasos)              # tiempo
bifmin=[]
bifmax=[]
bifmin2=[]
bifmax2=[]
X_est=zeros(len(t)/2)
X_est2=zeros(len(t)/2)
rangoc=linspace(0,500,501)
omegas=zeros(501)
contador=0
for a in rangoc:
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

 tau=lambda1+lambda2
 det=lambda1*lambda2
 omega=lambda1.imag
 omegas[contador]=omega
 contador=contador+1
 f4=p.figure(1)
 p.title('Frecuencia de ciclo')
 p.plot(rangoc,omegas)
 p.savefig('Frecuenciasa.png')