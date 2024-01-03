#!python
from numpy import *
import pylab as p
import nolds
from scipy import integrate 
from matplotlib import pyplot as plb 
from matplotlib import animation
from scipy.fftpack import fft, fftfreq, fftshift
# Definition of parameters
s=  15
a = 240
c = 25
phim=-15
phiM=15
omega=12.5
tini=0
tfin=120
tpasos=8001
paso=(tfin-tini)/tpasos
lyapul=[]
lyapvl=[]
U1=zeros(5)
V1=zeros(5)
j=0
X_f0 = array([ a/(5*c), c*(1+(a/(5*c))**2)])
lyapuvec=zeros(101)
lyapvvec=zeros(101)
T = paso
#xUf = np.linspace(0.0, tpasos*T, tpasos)
#xVf = np.linspace(0.0, tpasos*T, tpasos)
rangomega=linspace(20,40,21)
for omega in rangomega:
 phim=-phiM
 def phi(t):
     return 0.5*(phiM+phim+sin(omega*t)*(phim-phiM))
 def dX_dt(X, t):
 #""" Definimos la ecuacion . """
     return array([a-c*X[0]-4*X[0]*X[1]/(1+X[0]**2)-phi(t),
                   s*(c*X[0]-X[0]*X[1]/(1+X[0]**2)+phi(t))])
 #Colocamos los puntos fijos calculados 
 #Si son complejas los autovalores corresponden a frecuencias angulares 
 #Integramos con el modulo scipy 
 t = linspace(tini, tfin   ,  tpasos)              # tiempo
 X0 = array([0.01, 0.01])                     # condiciones iniciales 
 Z = integrate.odeint(dX_dt, X0, t,full_output=1)
 #Ploteamos la evolucion de las variables 
 F=Z[0]
 U=F[:,0] 
 V=F[:,1]
# Uf = fft(U)
# xUf = fftfreq(tpasos, T)
# xUf = fftshift(xUf)
# Uplot = fftshift(Uf)
# Uplot = fftshift(Uf)
# Vf = fft(V)
# xVf = fftfreq(tpasos, T)
# xVf = fftshift(xVf)
# Vplot = fftshift(Vf)
 f4=p.figure(3)
 p.plot(t, U, 'r-', label='U')
 plb.xlim(0,5)
 p.grid()
 p.legend(loc='best')
 p.xlabel('Tiempo')
 p.title('Evolucion temporal de U ,'+'omega :'+str(omega))
 f4.savefig('Upaso, omega ='+str(omega)+'.png')
 f5=p.figure(4)
 p.plot(t, V  , 'b-', label='V')
 plb.xlim(0,5)
 p.grid()
 p.legend(loc='best')
 p.xlabel('Tiempo')
 p.title('Evolucion temporal de V ')
 f5.savefig('Vpaso, omega ='+str(omega)+'.png')
 plb.close('all')
# f6=p.figure(5)
# p.plot(xUf, 1.0/paso * np.abs(Uplot))
# p.grid()
# p.title('Fourier U ,'+'omega :'+str(omega))
# plb.xlim([0,40])
# plb.ylim([0,0.5/paso * max(Uplot)])
# p.show()
# f7=p.figure(6)
# p.plot(xVf, 1.0/paso * np.abs(Vplot))
# p.grid()
# p.title('Fourier V ,'+'omega :'+str(omega))
# plb.ylim([0,1e07])
# plb.xlim([0,40])
# plb.savefig(str(omega)+'.jpg')
# f6.show()
#Las amplitudes quedan disgregadas entre 0 y 80 , a partir de ahí es ruido para las ultimas omegas
#Las omegas quedan en principio bien definidas entre 0 y 100
 #Dibujamos el espacio de fases 
 #
 #vcolores = p.cm.autumn_r(linspace(0.3, 1., len(valores)))

#Escogemos esos numeros decimales para expresar proximidad respecto al punto fijo
