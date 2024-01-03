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

def smooth(x,window_len=11,window='hanning'):
    """smooth the data using a window with requested size.
    
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal 
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.
    
    input:
        x: the input signal 
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
        
    example:

    t=linspace(-2,2,0.1)
    x=sin(t)+randn(len(t))*0.1
    y=smooth(x)
    
    see also: 
    
    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter
 
    TODO: the window parameter could be the window itself if an array instead of a string
    NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."


    if window_len<3:
        return x


    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"


    s=r_[x[window_len-1:0:-1],x,x[-2:-window_len-1:-1]]
    #print(len(s))
    if window == 'flat': #moving average
        w=ones(window_len,'d')
    else:
        w=eval('numpy.'+window+'(window_len)')

    y=convolve(w/w.sum(),s,mode='valid')
    return y







# Definition of parameters
s=  15
a = 240
c = 25
phim=-20
phiM=20
omega=1
tini=10
tfin=120
tpasos=4001 
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
rangomega=linspace(0,20,pasosomega)
rangophiM=linspace(0,50,11)
for phiM in rangophiM:
 graf=zeros((pasosomega,pasosomega))
 lyapul=[]
 lyapvl=[]
 lyapuvec=[]
 smoothlyapul=[]
 smoothlyapvl=[]
 lyapvvec=[]
 vectu=linspace(iniciou,finu,pasosomega)
 print(phiM)
 phim=-phiM
 for omega in rangomega:
  print(omega)
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
#  i=1
#  while i<len(U)-1:
#      if U[i]>U[i+1] and U[i]>U[i-1]:
#              j=int(round((omega-rangomega[0])/(rangomega[1]-rangomega[0])))
#              h=int(round((U[i]-iniciou)*(pasosomega-1)/(finu-iniciou)))
#              if h<=pasosomega-1 and h>0:
#                
#                graf[h,j]=graf[h,j]+1
#      i=i+1
  lyapu=nolds.lyap_r(U)
  lyapv=nolds.lyap_r(V)
  lyapul.append(lyapu)
  lyapvl.append(lyapv)
  if abs(lyapu)<=abs(lyapul[0]):
      lyapuvec.append(0)
  if abs(lyapv)<=abs(lyapvl[0]):
      lyapvvec.append(0)
  if abs(lyapu)>abs(lyapul[0]):
   if lyapu>0:
      lyapuvec.append(1)
   if lyapu<0:
      lyapuvec.append(-1)
  if abs(lyapv)>abs(lyapvl[0]):
   if lyapv>0:
      lyapvvec.append(1)
   if lyapv<0:
      lyapvvec.append(-1)
 p=0
# while p<pasosomega:
#    q=0
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
 smoothlyapul=smooth(lyapul)
 smoothlyapvl=smooth(lyapvl)
 f2=plb.figure(0,figsize=(17,8))
 f2, (ax1, ax2) = plb.subplots(2,figsize=(17,8))
 plb.grid(ax1)
 plb.grid(ax2)
 ax1.plot(rangomega,zeros(pasosomega),'r--')
 ax1.plot(rangomega, smoothlyapul)
 plb.subplots_adjust( hspace=0.1 )
 ax1.set_title('Lyapunov')
 ax2.scatter(rangomega, lyapuvec)

 f2.savefig('Lyapunov U, phiM= '+str(phiM)+'.png')
 
 f3=plb.figure(0,figsize=(17,8))
 f3, (ax1, ax2) = plb.subplots(2,figsize=(17,8))
 plb.grid(ax1)
 plb.grid(ax2)
 ax1.plot(rangomega,zeros(pasosomega),'r--')
 ax1.plot(rangomega, smoothlyapvl)
 plb.subplots_adjust( hspace=0.1 )
 ax1.set_title('Lyapunov')
 ax2.scatter(rangomega, lyapvvec)
`p.show()
 f2.savefig('Lyapunov V, phiM= '+str(phiM)+'.png')
 

