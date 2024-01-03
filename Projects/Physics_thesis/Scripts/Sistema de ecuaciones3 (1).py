#!python
from numpy import *
import pylab as p
from scipy import integrate 
from matplotlib import pyplot as plb 
from matplotlib import animation
# Definition of parameters
s=  20
a = 36
c = 1
phim=1
phiM=4.5
omega=0.25
tini=0
tfin=50
tpasos=101
paso=(tfin-tini)/tpasos
X_ahora=empty([tpasos,2])
X_f0 = array([ a/(5*c), c*(1+(a/(5*c))**2)])
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
X = integrate.odeint(dX_dt, X0, t, full_output=True)
#Ploteamos la evolucion de las variables 
F=X[0]
U=F[:,0] 
V=F[:,1]

f1 = p.figure(0)
p.plot(t, U, 'r-', label='U')
p.plot(t, V  , 'b-', label='V')
p.legend(loc='best')
p.xlabel('Tiempo')
p.title('Evolucion temporal de U y V')
f1.savefig('Evolucion Temporal.png')
#Dibujamos el espacio de fases 
#valores=linspace(0,2,11)
valores=0.2
vcolores = p.cm.autumn_r(linspace(0.3, 1., 1#len(valores)))
#Escogemos esos numeros decimales para expresar proximidad respecto al punto fijo
tprima=ones(5)
j=0
i=0
while j<5:
 tprima[j]=t[j]
 j=j+1
while len(tprima)<len(t):
 f3= p.figure(1)
 for v,col in zip(valores,vcolores):
   X0=v*X_f0
   X=integrate.odeint(dX_dt,X0,tprima)
   if v==0.2:
    print(X)
    print('---')
   p.plot(X [:,0],X[:,1],color=col,linewidth=1.5)
# Grideamos y ajustamos ejes 
 xmin,ymin=valores[0]*X_f0[0],valores[0]*X_f0[1]
 xmax,ymax=3*X_f0[0],3*X_f0[1]
 p.ylim(ymin,ymax)
 p.xlim(xmin,xmax)
 puntos=30
 x=linspace(xmin,xmax,puntos)
 y=linspace(ymin,ymax,puntos)
 tahora=t[-1]
  #Grideamos el quiver 
 X1,Y1=meshgrid(x, y)
 DX1, DY1 = dX_dt([X1, Y1],t=tahora)
 M = (hypot(DX1, DY1))
 M[ M == 0] = 1.
 DX1 /= M
 DY1 /= M
 p.title('Campo vectorial asociado ')
 p.grid()
 Q=p.quiver(X1, Y1, DX1, DY1, M, pivot='mid', cmap=p.cm.jet)
 f3.savefig('Campo vectorial,valor t= '+str(tprima[len(tprima)-1])+'.png')
 plb.close(f3)
 tprima=tprima.tolist()
 tprima.append(t[len(tprima)])
 tprima=asarray(tprima)
 print(len(tprima))


