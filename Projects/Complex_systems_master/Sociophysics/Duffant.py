
from numpy import *
import numpy as np
import pylab as p
import matplotlib
from scipy import integrate 
from matplotlib import pyplot as plb 
import random
tfinal=10000
numagentes=10
opiinf=0.5
error=zeros([numagentes])
matriz=zeros([numagentes,tfinal])
intercambios=ones([numagentes,numagentes])
gamma=empty([numagentes])
gammainf=empty([numagentes])
deltainf=empty([numagentes])
exito=zeros([numagentes])
delta=zeros([numagentes])
prueba=arange(0,numagentes)
tiempo=arange(1,tfinal)
agentes=arange(0,numagentes)
for i in agentes:
    matriz[i,0]=(i+1)/numagentes
    deltainf[i]=0.01
    delta[i]=0.01
for t in tiempo-1:
 j=random.choice(prueba)
 for i in agentes:
#Configuracion social 
  intercambios[i,j]+=1
  intercambios[j,i]=intercambios[i,j]
 intercambios[j,j]-=1
 success=0
 for i in agentes:
   exito[i]=0
   omega=20*pi/tfinal
   opiinf=0.4+0.2*random.uniform(0,1)
   n=0
 while success==0:
  n=n+1
  i=round(random.uniform(-0.5,numagentes-0.5))
  while exito[i]==1 :
   i=round(random.uniform(-0.5,numagentes-0.5))
   
  
  p=random.uniform(0,1)
  q=1
  if p>q:
   a=intercambios[i,i]/sum(intercambios[i,:])
   
   if abs(matriz[i,t]-opiinf)<a:
    matriz[i,t+1]=matriz[i,t]+deltainf[i]*(opiinf-matriz[i,t])
    intercambios[i,i]+=1
    exito[i]=1
    if matriz[i,t+1]>1:
       matriz[i,t+1]==1
    if matriz[i,t+1]<0:
       matriz[i,t+1]==0

  else:
    j=round(random.uniform(-0.5,numagentes-0.5))
    b=intercambios[i,j]/sum(intercambios[i,:])
    c=intercambios[i,j]/sum(intercambios[j,:])
    if abs(matriz[i,t]-matriz[j,t])<b and abs(matriz[j,t]-matriz[i,t])<c and i!=j:
      matriz[i,t+1]=matriz[i,t]+delta[i]*(matriz[j,t]-matriz[i,t])
      matriz[j,t+1]=matriz[j,t]+delta[j]*(matriz[i,t]-matriz[j,t])
      if matriz[j,t+1]>1:
       matriz[j,t+1]==1
      if matriz[i,t+1]>1:
       matriz[i,t+1]==1
      if matriz[j,t+1]<0:
       matriz[j,t+1]==0
      if matriz[i,t+1]<0:
       matriz[i,t+1]==0
      intercambios[i,j]+=1
      intercambios[j,i]+=1
      exito[i]=1
      exito[j]=1
    
  for k in agentes:
           if q>0 and q<1:
            b=intercambios[i,k]/sum(intercambios[i,:])
            if not(abs(matriz[i,t]-matriz[k,t])<b) and k!=i and not(abs(matriz[i,t]-opiinf)<a):
                matriz[i,t+1]=matriz[i,t]
                exito[i]=1
           if q==1: 
            b=intercambios[i,k]/sum(intercambios[i,:])
            if not(abs(matriz[i,t]-matriz[k,t])<b) and k!=i :
                matriz[i,t+1]=matriz[i,t]
                exito[i]=1
           if q==0:
            if not(abs(matriz[i,t]-opiinf)<gamma[i]) and k!=i :
                matriz[i,t+1]=matriz[i,t]
                exito[i]=1
  if all(exito)==1:

       success=1
f1=plb.figure()
for i in agentes:
 plb.plot(matriz[i,:])
 plb.xlabel('Tiempo')
f2=plb.figure()
plb.imshow(intercambios)
plb.colorbar()
f1.savefig('Evoluciontemporal_3 .png')
f2.savefig('Intecambios_3.png')
