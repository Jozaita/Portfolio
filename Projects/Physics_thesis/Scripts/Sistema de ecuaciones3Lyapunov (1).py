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
tpasos=4001 
paso=(tfin-tini)/tpasos
iniciou=100
finu=225
pasosomega=2001
pasosu=2001
num=5
interruptor=1
graf=zeros((pasosomega,pasosu))
grafsmooth=zeros((int(pasosomega/num),pasosomega))
j=0
h=0
b=0
X_f0 = array([ a/(5*c), c*(1+(a/(5*c))**2)])
lyapuvec=zeros(pasosomega)
lyapvvec=zeros(pasosomega)
orbitas=zeros((pasosomega,pasosomega))
vectu=linspace(iniciou,finu,pasosu)
rangomega=linspace(16.25,16.4,pasosomega)
rangophiM=[10]
total=pasosomega**2
orbitas=zeros(pasosomega)
contador=0
for phiM in rangophiM:
 graf=zeros((pasosomega,pasosu))
 lyapul=[]
 lyapvl=[]
 vectu=linspace(iniciou,finu,pasosomega)
 phim=-phiM
 for omega in rangomega:
  def phi(t):
      return 0.5*(phiM+phim+sin(omega*t)*(phim-phiM))
  def dX_dt(X, t):
  #""" Definimos la ecuacion . """
      return array([a-c*X[0]-4*X[0]*X[1]/(1+X[0]**2)-phi(t),
                    s*(c*X[0]-X[0]*X[1]/(1+X[0]**2)+phi(t))])   

  def dX1_dt(X, t):
  #""" Definimos la ecuacion . """
      return array([a-c*X[0]-4*X[0]*X[1]/(1+X[0]**2),
                    s*(c*X[0]-X[0]*X[1]/(1+X[0]**2))])   

    
  t = linspace(tini, tfin   ,  tpasos)              # tiempo
  X0 = array([0.01, 0.01])                     # condiciones iniciales 
  Z = integrate.odeint(dX_dt, X0, t,full_output=1)
  B= integrate.odeint(dX1_dt, X0, t,full_output=1)
  #Ploteamos la evolucion de las variables 
  F=Z[0]
  U=F[:,0] 
  V=F[:,1]

  V=V[len(V)/8:]
  i=1
  print(str(phiM ), str(omega))

  while i<len(V)-1:
      if V[i]>V[i+1] and V[i]>V[i-1]:
              j=int(round((omega-rangomega[0])/(rangomega[1]-rangomega[0])))
              h=int(round((V[i]-iniciou)*(pasosu-1)/(finu-iniciou)))
              if h<=pasosomega-1 and h>0:
                
                graf[h,j]=graf[h,j]+1
            
      i=i+1
# k=0
# anchura=2
# for j in rangomega:
#  while k<pasosomega-1:
#   if graf[k,j]!=0 and graf[k+1,j]==0:
#    print(k)
#    orbitas[j]=orbitas[j]+1
#    k=k+1
#   k=k+1
#  b=int(round((phiM-rangophiM[0])/(rangophiM[1]-rangophiM[0])))
  #
  
#   multiplos=arange(0,pasosomega-4,num)
#   for l in multiplos:
#     l=int(l)
#     ll=int(l/num)
#     grafsmooth[ll,j]=(graf[l,j]+graf[l+1,j]+graf[l+2,j]+graf[l+3,j]+graf[l+4,j])/num
  
#   dist=round(pasosomega/num*0.08)
#   k=peakutils.indexes(grafsmooth[:,j], thres=0.2, min_dist=dist)
#   orbitas[j,b]=len(k)
  
#   f7=plb.figure(8)
#   contador=contador+1
 p=0
 while p<pasosu:
    q=0
    renorm=sum(graf[:,p])
    average=renorm/pasosomega
    while q<pasosomega:
     if graf[q,p]!=0:
        graf[q,p]=graf[q,p]/renorm
     if graf[q,p]==0:
         graf[q,p]=-1000
     q=q+1
    p=p+1

 f1=plb.figure(0,figsize=(17,8))
 cs=plb.pcolormesh(rangomega, vectu,graf[:,:],cmap='YlOrRd')
# cs=plb.imshow(graf,cmap='YlOrRd')
 plb.title('Maximos')
  # set the limits of the plot to the limits of the data
 plb.title('PhiM = '+str(phiM))
 plb.colorbar()
 f1.savefig('Maximos4nuevo= '+str(rangomega[-1])+'.png')

 plb.close('all')
#f2=plb.figure(0,figsize=(17,8))
#cs=plb.pcolormesh(rangophiM, rangomega,orbitas[:,:],cmap='gist_rainbow')
#plb.colorbar()
#plb.title('Orbitas')
#f2.savefig('Orbitasmap.png')

#plb.close('all')
