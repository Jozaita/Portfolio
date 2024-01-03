
from numpy import *
import numpy as np
import pylab as p
import matplotlib
from scipy import integrate 
from matplotlib import pyplot as plb 
tfinal=1000  
numagentes=10

simulaciones=arange(1,11)

intercambios=zeros([numagentes,numagentes])
intercambiosinf=zeros([numagentes])
opinionfinal=zeros([11,11])
gamma=empty([numagentes])
delta=empty([numagentes])
tiempo=arange(1,tfinal)
agentes=arange(0,numagentes)
gammainf=empty([numagentes])
deltainf=empty([numagentes])
exito=zeros([numagentes])
opinionfinal=zeros([11,11])
ngamma=linspace(0.1,0.5,11)
ndelta=linspace(0.1,0.5,11)
for g in ngamma:
 for d in ndelta:
  for n in simulaciones:
   print(g,d,n)
   matriz=zeros([numagentes,tfinal])
   for i in agentes:
    
    matriz[i,0]=random.uniform()
    gammainf[i]=d
    deltainf[i]=random.uniform()
    gamma[i]=g
    delta[i]=deltainf[i]
   for t in tiempo-1:
    omega=20*pi/tfinal
    opiinf=0.5+0.1*sin(omega*t)
    success=0
    for i in agentes:
      exito[i]=0
    while success==0:
     i=round((numagentes-1)*random.uniform())
  
     p=random.uniform()
     q=0.5
     if p>q:
      if abs(matriz[i,t]-opiinf)<gammainf[i]:
       matriz[i,t+1]=matriz[i,t]+deltainf[i]*(opiinf-matriz[i,t])
       intercambios[i,i]=1
       exito[i]=1
       if matriz[i,t+1]>1:
          matriz[i,t+1]==1
       if matriz[i,t+1]<0:
          matriz[i,t+1]==0

     else:
       j=round((numagentes-1)*random.uniform())
       if abs(matriz[i,t]-matriz[j,t])<gamma[i] and abs(matriz[j,t]-matriz[i,t])<gamma[j] and i!=j:
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
         intercambios[i,j]=1
         intercambios[j,i]=1
         exito[i]=1
         exito[j]=1
    
     for k in agentes:
              if q>0 and q<1:
               if not(abs(matriz[i,t]-matriz[k,t])<gamma[i]) and k!=i and not(abs(matriz[i,t]-opiinf)<gamma[i]):
                   matriz[i,t+1]=matriz[i,t]
                   exito[i]=1
              if q==1:
               if not(abs(matriz[i,t]-matriz[k,t])<gamma[i]) and k!=i :
                   matriz[i,t+1]=matriz[i,t]
                   exito[i]=1
              if q==0:
               if not(abs(matriz[i,t]-opiinf)<gamma[i]) and k!=i :
                   matriz[i,t+1]=matriz[i,t]
                   exito[i]=1
     if all(exito)==1:

          success=1
#f1=plb.figure()
#for i in agentes:
# plb.plot(matriz[i,:])
#f2=plb.figure()
#plb.imshow(intercambios)
   histo=histogram(matriz[:,t+1],numagentes,range=[0,1])
   histo=histo[0]
   for k in agentes:
       if histo[k]!=0:
          
          a=int((g-0.1)/(ngamma[1]-ngamma[0])+0.1)
          b=int((d-0.01)/(ndelta[1]-ndelta[0])+0.1)
          opinionfinal[a,b]=opinionfinal[a,b]+1
#f1=p.figure()
#for i in agentes:
# p.plot(matriz[i,:])
#f2=p.figure()
#plb.imshow(intercambios)
for a in arange(0,11):
    for b in arange(0,11):
        opinionfinal[a,b]=opinionfinal[a,b]/simulaciones[-1]
f1=plb.figure(figsize=(17,8))
plb.imshow(opinionfinal)
f1.savefig('Opinion final2_5_f.png')
np.savetxt('Duffant continuo2_5_f', opinionfinal)