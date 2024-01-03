#!python
from numpy import *
import pylab as p
from scipy import integrate 
from matplotlib import pyplot as plb 
from matplotlib import animation
from scipy.fftpack import fft, fftfreq, fftshift
# Definition of parameters
s=  15
a = 240
c = 25
tini=0
tfin=80
tpasos=2000
recta=zeros(30)
bifmin=[]
bifmax=[]
rangoc=[25]
paso=(tfin-tini)/tpasos
T = paso
xUf = linspace(0.0, tpasos*T, tpasos)
xVf = linspace(0.0, tpasos*T, tpasos)
for c in rangoc:
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
 print(c)
 Uf = fft(U)
 xUf = fftfreq(tpasos, T)
 xUf = fftshift(xUf)
 Uplot = fftshift(Uf)
 Vf = fft(V)
 xVf = fftfreq(tpasos, T)
 xVf = fftshift(xVf)
 Vplot = fftshift(Vf)
 f6=p.figure(5)
 p.plot(xUf, 1.0/paso *abs(Uplot),linewidth=2)
 p.grid()
 p.title('Fourier U ,'+'c :'+str(a))
 plb.xlim([0,13])
 plb.ylim([0,0.5/paso * max(Uplot)])
 p.show()
 f6.savefig('FU-c='+str(c)+'.jpg')
 f7=p.figure(6)
 p.plot(xVf, 1.0/paso *abs(Vplot),linewidth=2)
 p.grid()
 p.title('Fourier V ,'+'c :'+str(c))
 plb.ylim([0,0.5/paso * max(Vplot)])
 plb.xlim([0,13])
 f7.savefig('FV-c='+str(c)+'.jpg')
 udib=1.0/paso *abs(Uplot)
 vdib=1.0/paso *abs(Vplot)
 

