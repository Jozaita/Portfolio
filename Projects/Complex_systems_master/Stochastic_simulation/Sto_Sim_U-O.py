import numpy as np
import matplotlib
from scipy import integrate 
from matplotlib import pyplot as plb
import random

trayec=10
tiempo=10
a_2=2
d=0.05
h=0.01
tau=0.005
num=int(tiempo/h)
matrix=np.zeros([num,trayec])
matrix[0,:]=1
for i in range(0,trayec):
 hor=[]
 ver=[]
 p=np.exp(-h/tau)
 b=-np.sqrt(tau/2)*(1-p)*random.gauss(0,1)
 gh=0
 a=0
 x=1
 alpha=np.sqrt(h)
 beta=-tau*(1-p)/np.sqrt(h)
 gamma=np.sqrt(tau*(1-p*p)/2-tau*tau*(1-p)*(1-p)/h)
 for t in range(1,num):
  a_old=a
  b_old=b
  def q(x):
     return -a_2*x
 #Generation of gh
  u=random.gauss(0,1)
  v=random.gauss(0,1)
  a=alpha*u
  b=beta*u+gamma*v
  gh=p*gh-p*a_old+a-b_old+b
  aux=h*q(x)+gh*np.sqrt(d)
  x=x+0.5*(aux+h*q(x+aux)+gh*np.sqrt(d))
  matrix[t,i]=x
f1=plb.figure()
plb.xlabel('Time')
plb.ylabel('dx/dt')
plb.title('Tau='+str(tau))
for i in range(0,trayec):
    plb.plot(matrix[:,i])
f1.savefig('Sto_Sim_3.png')
    

 
 