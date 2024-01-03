#!python
from numpy import *
import pylab as p
from scipy import integrate 
from matplotlib import pyplot as plb 
from matplotlib import animation
from mpl_toolkits.mplot3d.axes3d import Axes3D, get_test_data
from matplotlib import cm
# Definition of parameters

s=  15
a = 240
c = 60
tini=0
tfin=60
tpasos=1001
t = linspace(tini, tfin   ,  tpasos)              # tiempo

fig = plb.figure(figsize=(17,8))
ax = fig.add_subplot(1, 2, 1, projection='3d')

X = arange(0,50, 0.25)
Y = arange(0,50, 0.25)
X, Y =meshgrid(X, Y)
R =sqrt(X**2 + Y**2)
Z = (5/6)*(Y+sqrt(Y**2+60*X**2))
X1=arange(0,50,0.25)
Y1=linspace(15,15,len(X1))
Z1=linspace(240,240,len(X1))
X2=linspace(25,25,len(X1))
Y2=linspace(15,15,len(X1))
Z2=linspace(0,400,len(X1))
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
ax.plot(X1, Y1, Z1,'r--', label='parametric curve',linewidth=3)
ax.plot(X2, Y2, Z2,'g--', label='parametric curve',linewidth=3)
ax.set_xlabel('C')
ax.set_ylabel('$\sigma$',fontsize=20)
ax.set_zlabel('A')
for angle in range(0, 360):
    ax.view_init(30, angle)
    plb.draw()
    fig.savefig('Espaciobif3d'+str(angle)+'.jpg')
    plb.pause(.001)
plb.show()

fig.savefig('Espaciobif3d.jpg')
