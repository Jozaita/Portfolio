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
import matplotlib.pyplot as plb
# Definition of parameters
s=  15
a = 240
c = 25
phim=-20
phiM=20
omega=1
tini=0
tfin=120
tpasos=4000
paso=(tfin-tini)/tpasos
iniciou=0  
finu=8
pasosomega=2001
graf=zeros((pasosomega,pasosomega))
j=0
X_f0 = array([ a/(5*c), c*(1+(a/(5*c))**2)])
lyapuvec=zeros(pasosomega)
lyapvvec=zeros(pasosomega)
orbitas=zeros(pasosomega)
vectu=linspace(iniciou,finu,pasosomega)
rangomega=linspace(12.5,15,pasosomega)
rangophiM=[10]
for phiM in rangophiM:
 graf=zeros((pasosomega,pasosomega))
 entuvec=[]
 entvvec=[]
 lyapuvec=zeros(pasosomega)
 lyapvvec=zeros(pasosomega)
 vectu=linspace(iniciou,finu,pasosomega)
 phim=-phiM
 for omega in rangomega:
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

#  i=1
#  while i<len(U)-1:
#      if U[i]>U[i+1] and U[i]>U[i-1]:
  j=int(round((omega-rangomega[0])/(rangomega[1]-rangomega[0])))
  print(str(int(j)/(pasosomega-1)*100)+' %')
#              h=int(round((U[i]-iniciou)*(pasosomega-1)/(finu-iniciou)))
#              if h<=pasosomega-1 and h>0:
#                
#                graf[h,j]=graf[h,j]+1
#      i=i+1
#  entu=nolds.lyap_r(U1)
  entv=nolds.sampen(V1)
#  entuvec.append(entu)
  entvvec.append(entv)
  mediau=0.0034981316456359798
  mediav=0.0017402573427756172
  desviacionu=0.0059526964517817825
  desviacionv=0.0029168686357234032
#  if entu>mediau+2*desviacionu:
#      lyapuvec[j]=1
  if entv>mediav+4*desviacionv:
      lyapvvec[j]=1
#  if entu==mediau:
#      lyapuvec[j]=0
#  if entu<mediau-2*desviacionu:
#      lyapuvec[j]=-1
  if entv<mediav-4*desviacionv:
      lyapvvec[j]=-1
  if entv==mediav:
      lyapvvec[j]=0


# while p<pasosomega:
#    q=00.0018365123583663468
#    renorm=sum(graf[:,p])
#    average=renorm/pasosomega
#    while q<pasosomega:
#     if graf[q,p]!=0:
#        graf[q,p]=graf[q,p]/renorm
#     if graf[q,p]==0:
#         graf[q,p]=-1000
#     q=q+1
#    p=p+1

# f1=plb.figure(0,figsize=(17,8))
# cs=plb.pcolormesh(rangomega, vectu,graf[:,:],cmap='YlOrRd')
# plb.title('Maximos')
  # set the limits of the plot to the limits of the data
# plb.title('PhiM = '+str(phiM))
# plb.colorbar()
# f1.savefig('Maximos,phiM= '+str(phiM)+'.png')
# plb.close('all')
# mediau=np.average(entuvec)
# mediav=np.average(entvvec)
# desviacionu=np.std(entuvec)
# desviacionv=np.std(entvvec)
# f2, axarr = plb.subplots(2, sharex=True,figsize=(17, 8))
# axarr[0].set_xlim([0,20])
# axarr[1].set_xlim([0,20])
# axarr[0].grid(True)
# axarr[1].grid(True)
# axarr[0].plot(rangomega, entuvec)
# axarr[0].set_title('Lyapunov U')
# axarr[1].scatter(rangomega,lyapuvec)
# f2.savefig('Lyapunov U prueba, phiM= '+str(phiM)+'.png')
# plb.close(f2)
 f3= plb.figure(1,figsize=(17, 8)) #sharex=True
 axarr[0].set_xlim([12.5,15])
 axarr[1].set_xlim([12.5,15])
 p.grid(True)
 axarr[1].grid(True)
 p .plot(rangomega, entvvec,'b')
 p.title('Entropia V')
 axarr[1].scatter(rangomega,lyapvvec)
 f3.savefig('Lyapunov V prueba ampli  , phiM= '+str(rangomega[-1])+'.png')
 plb.close('all')

    