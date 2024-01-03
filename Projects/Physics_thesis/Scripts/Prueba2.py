#!python
from numpy import *
import pylab as p
from scipy import integrate 
# Definition of parameters
s = 1.
a = 50
c = 1
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
#Si son complejas los autovalores corresponden a frecuencias angulares 
if type(lambda1)==complex128 :
    T_f1 = 2*pi/abs((lambda1.imag))
if type(lambda2)==complex128 :
    T_f2 = 2*pi/abs((lambda2.imag))
#Integramos con el modulo scipy 
t = linspace(0, 150,  1000)              # tiempo
X0 = array([10, 5])                     # condiciones iniciales 
X = integrate.odeint(dX_dt, X0, t, full_output=True)
#Ploteamos la evolucion de las variables 
F=X[0]
U=F[:,0]
V=F[:,1]
f1 = p.figure()
p.plot(t, U, 'r-', label='U')
p.plot(t, V  , 'b-', label='V')
p.grid()
p.legend(loc='best')
p.xlabel('Tiempo')
p.title('Evolucion temporal de U y V')
f1.savefig('Evolucion Temporal.png')
#Dibujamos el espacio de fases 
valores=linspace(-1,1,20)
vcolores = p.cm.autumn_r(linspace(0.3, 1., len(valores)))
fig2=p.figure()
#Escogemos esos numeros decimales para expresar proximidad respecto al punto fijo
for v,col in zip(valores,vcolores):
    X0=v*X_f0
    X=integrate.odeint(dX_dt,X0,t)
    p.plot(X[:,0],X[:,1],color=col)
#Grideamos y ajustamos ejes 
xmin,ymin=-50*X_f0
xmax,ymax=50*X_f0
p.ylim(ymin,ymax)
p.xlim(xmin,xmax)
puntos=30
x=linspace(xmin,xmax,puntos)
y=linspace(ymin,ymax,puntos)
#Grideamos el quiver 
X1,Y1=meshgrid(x, y)
DX1, DY1 = dX_dt([X1, Y1])
M = (hypot(DX1, DY1))
M[ M == 0] = 1.
DX1 /= M
DY1 /= M
p.title('Campo vectorial asociado ')
Q = p.quiver(X1, Y1, DX1, DY1, M, pivot='mid', cmap=p.cm.jet)

