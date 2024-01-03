#!python
from numpy import *
import numpy as np
import pylab as p
import nolds
import matplotlib
from scipy import integrate 
from matplotlib import pyplot as plb 
from matplotlib import animation
from scipy.fftpack import fft
from scipy import signal
import peakutils 
from peakutils.plot import plot as pplot
# Definition of parameters
s=  15
a = 240
c = 25
phim=-5
phiM=5
omega=1
tini=0
tfin=120
tpasos=4000
paso=(tfin-tini)/tpasos
iniciou=50
finu=300
rangomega=arange(0,101,0.1)
rangophiM=arange(0,51,1)
pasosomega1=len(rangomega)
pasosomega2=len(rangophiM)
num=3
graf=zeros((pasosomega2,pasosomega1))
grafsmooth=zeros((int(pasosomega2/num),pasosomega1))
j=0
X_f0 = array([ a/(5*c), c*(1+(a/(5*c))**2)])
lyapuvec=zeros(pasosomega)
lyapvvec=zeros(pasosomega)
orbitasu=zeros((pasosomega1,pasosomega2))
orbitasv=zeros((pasosomega1,pasosomega2))
orbitaslyapu=zeros((pasosomega1,pasosomega2))
orbitaslyapv=zeros((pasosomega1 ,pasosomega2))
vectu=linspace(iniciou,finu,pasosomega)
graf=zeros((pasosomega2,pasosomega1))
for phiM in rangophiM:
 lyapul=[]
 lyapvl=[]
 entuvec=[]
 entvvec=[]
 lyapuvec=[]
 lyapvvec=[]
 vectu=linspace(iniciou,finu,pasosomega)
 phim=-phiM
 for omega in rangomega:
  print(phiM , omega)
  def phi(t):
      return 0.5*(phiM+phim+sin(omega*t)*(phim-phiM))
  def dX_dt(X, t):
  #""" Definimos la ecuacion . """
      return array([a-c*X[0]-4*X[0]*X[1]/(1+X[0]**2)-phi(t),
                    s*(c*X[0]-X[0]*X[1]/(1+X[0]**2)+phi(t))])   

  t = linspace(tini, tfin   ,  tpasos)              # tiempo
  X0 = array([0.01, 0.01])                     # condiciones iniciales 
  Z = integrate.odeint(dX_dt, X0, t,full_output=1)
  #Ploteamos la evolucion de las variables 
  F=Z[0]
  U=F[:,0] 
  V=F[:,1]
  U1=U[len(U)/8:]
  V1=V[len(V)/8:]
  i=1
#  while i<len(V1)-1:
 #     if V1[i]>V1[i+1] and V1[i]>V1[i-1]:
  j=int(round((omega-rangomega[0])/(rangomega[1]-rangomega[0])))
#              h=int(round((V1[i]-iniciou)*(pasosomega-1)/(finu-iniciou)))
#              if h<=pasosomega-1 and h>0:
                
#                graf[h,j]=graf[h,j]+1
#      i=i+1
  b=int(round((phiM-rangophiM[0])/(rangophiM[1]-rangophiM[0])))
  entu=nolds.sampen(U1)
  entv=nolds.sampen(V1)
  orbitasu[j,b]=entu
  orbitasv[j,b]=entv
  orbitaslyapu[j,b]=nolds.lyap_r(U1)
  orbitaslyapv[j,b]=nolds.lyap_r(V1)
  print(orbitasv[j,b])
  print(orbitaslyapv[j,b])

 plb.close('all')
f   2=plb.figure(2,figsize=(17,8))
cs=plb.pcolormesh(rangophiM, rangomega,orbitasu[:,:],cmap='gist_rainbow')
plb.colorbar()
plb.title('Orbitas')
f2.savefig('Orbitasumap.png')

plb.close('all')
f3=plb.figure(1,figsize=(   17,8))
cs=plb.pcolormesh(rangophiM, rangomega,orbitasv[:,:],cmap='gist_rainbow')
plb.colorbar()
plb.title('Orbitas')
f3.savefig('Orbitasvmap.png')

plb.close('all')
f4=plb.figure(5,figsize=(17,8))
cs=plb.pcolormesh(rangophiM, rangomega,orbitaslyapu[:,:],cmap='gist_rainbow')
plb.colorbar()
plb.title('Orbitas')
f4.savefig('Orbitaslyapumap.png')

plb.close('all')

f5=plb.figure(6,figsize=(17,8))
cs=plb.pcolormesh(rangophiM, rangomega,orbitaslyapv[:,:],cmap='gist_rainbow')
plb.colorbar()
plb.title('Orbitas')
f5.savefig('Orbitaslyapvmap.png')
