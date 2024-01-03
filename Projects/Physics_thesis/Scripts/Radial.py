# -*- coding: utf-8 -*-
"""
Created on Fri May 26 19:12:40 2017

@author: user
"""

#!python
from numpy import *
import pylab as p
from scipy import integrate 
from matplotlib import pyplot as plb 
from matplotlib import animation
from mpl_toolkits.mplot3d.axes3d import Axes3D, get_test_data
from matplotlib import cm
# Definition of parameters
a=240
s=25
c=15
angini=(pi/2)*0.01
ang=pi/2
angulos=linspace(angini,ang,2000)
radios=arange(1,100,1)
rderiv=arange(1,201,1)
thetaderiv=arange(1,2001,1)
rzeros=[]
R=zeros(2)
contador=0
def rpunto(R):
    return cos(R[1])*(a+R[0]*c*(s*sin(R[1])-cos(R[1]))-1/(1/R[0]**2+cos(R[1])**2)*(sin(R[1])*(4*cos(R[1])+s*sin(R[1]))))

def thetapunto(R):
    return 0.5*sin(2*R[1])*(c-R[0]/(1+R[0]**2*cos(R[1])**2)*(s*cos(R[1])-4*sin(R[1])))+s*c*cos(theta)**2-a*sin(R[1])/(R[0])
for r in radios:
    contador=0
    for theta in angulos:
        R[0]=r
        R[1]=theta
        thetaderiv[contador]=thetapunto(R)
        contador=contador+1
    f1=p.figure()
    p.title('radio :'+ str(R[0]))
    p.plot(angulos,thetaderiv)
    p.plot(angulos,zeros(len(angulos)))
    p.savefig(str(R[0])+'.jpg')
    p.show()
    p.close('all')
#for theta in angulos:
#    for r in radios:
#        R[0]=r
#        R[1]=theta
#        rderiv[r-1]=rpunto(R)
#    f1=p.figure()
#    p.plot(radios,rderiv,linewidth=3)
#    p.plot(radios,zeros(len(radios)))
#    p.xlim([0,400])
#    p.ylim([-100,100])
#    p.xlabel('r')
#    p.ylabel('rpunto')
#    p.title('Angulo : '+str(theta*360/(2*pi)))
#    f1.savefig(str(theta*360/(2*pi))+'.png')
#    p.close('all')
    