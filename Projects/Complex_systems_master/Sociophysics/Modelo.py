
from numpy import *
import numpy as np
import pylab as p
import matplotlib
from scipy import integrate 
from matplotlib import pyplot as plb 
# Definition of parameters
informador=random.uniform()
d={}
consensos=[]
confmedia=[]
opimedia=[]
varconf=[]
varopi=[]
numero =arange(0,10)
opi=zeros(numero[-1])
alpha=zeros(numero[-1])
beta=zeros(numero[-1])
gama=zeros(numero[-1])
delta=ones(numero[-1])
veces=arange(1,2*10**5)
for i in numero-1:
 alpha[i]=0.5
 beta[i]=0.5
 gama[i]=0.15
 delta[i]=random.normal(0.005,0.002)
    
for  n in veces : 
 print(n)    
 disenso=0
 consenso=0
 for i in numero-1 :
            d["string{0}".format(i)]="informado"+str(i)
            informado=random.uniform()
            opi[i]=(alpha[i]*informador+beta[i]*informado)/(alpha[i]+beta[i])
            
            if abs(opi[i]-informador)>=gama[i]:
              alpha[i]=alpha[i]-delta[i]
              beta[i]=beta[i]+delta[i]
              if alpha[i]<0:
                  alpha[i]=0
              if beta[i]>1:
                  beta[i]=1
                  
            else :
              consenso=consenso+1
              alpha[i]=alpha[i]+delta[i]
              beta[i]=beta[i]-delta[i]
              if alpha[i]>1:
                  alpha[i]=1
              if beta[i]<0:
                  beta[i]=0
 confmedia.append(average(alpha)) 
 consensos.append(consenso)
 opimedia.append(average(opi))
 varconf.append(var(alpha))
 varopi.append(var(opi))
            
            
    