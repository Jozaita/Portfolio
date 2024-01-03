#!python
from numpy import *
import pylab as p
from scipy import integrate 
from matplotlib import pyplot as plb 
from matplotlib import animation
from scipy.fftpack import fft, fftfreq, fftshift
# Definition of parameters
s=  15
pararaba
a = 240
c = 25
tini=0
tfin=5
tpasos=2000
recta=zeros(30)
bifmin=[]
bifmax=[]
rangoc=arange(1,240,1)
paso=(tfin-tini)/tpasos
T = paso
xUf = linspace(0.0, tpasos*T, tpasos)
xVf = linspace(0.0, tpasos*T, tpasos)
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
 #Si son complejas los autovalores corresponden a frecuencias angulares 
 if type(lambda1)==complex128 :
     T_f1 = 2*pi/abs((lambda1.imag))
 if type(lambda2)==complex128 :
     T_f2 = 2*pi/abs((lambda2.imag))
 #Integramos con el modulo scipy 
 t = linspace(tini, tfin   ,  tpasos)              # tiempo
 X0 = array([10, 5])                     # condiciones iniciales 
 X = integrate.odeint(dX_dt, X0, t, full_output=True)
 #Ploteamos la evolucion de las variables 
 F=X[0]
 U=F[:,0]
 V=F[:,1]
 f1 = p.figure(0)
 p.plot(t, U, 'r-', label='U')
 p.plot(t, V  , 'b-', label='V')
 p.grid()
 p.legend(loc='best')
 p.xlabel('Tiempo')
 p.title('Evolucion temporal de U y V')
 f1.savefig('1Evolucion Temporal,valor a='+str(a)+'.png')
#Dibujamos el espacio de fases 
 f2= p.figure(1)
 valores=linspace(0,50,50)
 vcolores = p.cm.autumn_r(linspace(0.3, 1., len(valores)))
 #Escogemos esos numeros decimales para expresar proximidad respecto al punto fijo
# for v,col in zip(valores,vcolores):
 X0=[8,250]
 X=integrate.odeint(dX_dt,X0,t)
 p.plot(X[:,0],X[:,1],color='r',linewidth=2)
 #Grideamos y ajustamos ejes 
 xmin,ymin=0,0.6*X_f0[1]
 xmax,ymax=5,1.8*X_f0[1]
 p.ylim(ymin,ymax)
 p.xlim(xmin,xmax)
 puntos=30
 x=linspace(xmin,xmax,puntos)
 y=linspace(ymin,ymax,puntos)
 i=0
 #Grideamos el quiver 
 X1,Y1=meshgrid(x, y)
 DX1, DY1 = dX_dt([X1, Y1])
 M = (hypot(DX1, DY1))
 M[ M == 0] = 1.
 DX1 /= M
 DY1 /= M
 print(a)
 p.title('Campo vectorial asociado  ,'+str(s))
 if u=
 Q=p.quiver(X1, Y1, DX1, DY1, M, pivot='mid', cmap=p.cm.jet)
 p.plot(X[:,0],X[:,1],linewidth=2)
 #Vamos a intentar animarlo 
 u=linspace(0,xmax,100)
 #Definimos las nullclines 
 def f(u):
      return (a-c*u)*((1+u**2)/(4*u))
 def g(u):
      return c*(1+u**2)
 f2=p.figure(1)
 p.plot(u,f(u),linewidth=1.5,label='U punto = 0')
 p.plot(u,g(u),linewidth=1.5,label='V punto = 0')
 p.grid()
 p.legend(loc='lower right')
 f2.savefig('1Campo vectorial,valor a= '+str(a)+'.png')
 p.close('all')