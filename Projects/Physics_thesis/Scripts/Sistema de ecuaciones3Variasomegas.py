#!python
from numpy import *
import pylab as p
import nolds
from scipy import integrate 
from matplotlib import pyplot as plb 
from matplotlib import animation
# Definition of parameters
s=  15
a = 240
c = 25
phim=-10
phiM=10
omega=1
tini=0
 tfin=30
tpasos=4001
paso=(tfin-tini)/tpasos
pasosomega=1501
rangomega=linspace(9,16.5,pasosomega)
U1=zeros(5)
V1=zeros(5)
X_f0 = array([ a/(5*c), c*(1+(a/(5*c))**2)])
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
 X0 = array([10, 5])                     # condiciones iniciales 
 Z = integrate.odeint(dX_dt, X0, t)
 #Ploteamos la evolucion de las variables 
 F=Z[0]
 U=Z[:,0] 
 V=Z[:,1]
 f5, axarr = p.subplots(2, sharex=True)
 axarr[0].plot(t, U)
 axarr[0].set_title('Evolucion U y V')
 axarr[1].plot(t, V)
 axarr[0].set_xlim(0,5)
 axarr[1].set_xlim(0,5)
 f5.savefig('Evolucion separadaomega='+str(omega)+' .png')
 plb.close(f5)
 #Dibujamos el espacio de fases 
 #
 #valores=linspace(0,2,11)
 #vcolores = p.cm.autumn_r(linspace(0.3, 1., len(valores)))

 #Escogemos esos numeros decimales para expresar proximidad respecto al punto fijo
 f3= p.figure(1)
 #for v,col in zip(valores,vcolores):
 X0=4*X_f0
# Grideamos y ajustamos ejes 
 V1=V[len(V)/8:]
 U1=U[len(U)/8:]
 xmin,ymin=min(U1)*0.8,min(V1)*0.8
 xmax,ymax=max(U1)*1.2,max(V1)*1.2
 p.ylim(ymin,ymax)
 p.xlim(xmin,xmax)
 puntos=30
 x=linspace(xmin,xmax,puntos)
 y=linspace(ymin,ymax,puntos)
 tahora=t[-1]
  #Grideamos el quiver 
 X1,Y1=meshgrid(x, y)
 DX1, DY1 = dX_dt([X1, Y1],puntos)
 M = (hypot(DX1, DY1))
 M[ M == 0] = 1.
 DX1 /= M
 DY1 /= M
 p.title('Campo vectorial asociado ')
 p.grid()
 jet= plb.get_cmap('jet')
 jet = cm = plb.get_cmap('jet') 
 Q=p.quiver(X1, Y1, DX1, DY1, M, pivot='mid',cmap=jet)
 T=p.plot(U,V,'g')
 f3.savefig('Campo vectorial,omega='+str(omega)+' .png')
 print(omega)
 plb.close(f3)



###############################