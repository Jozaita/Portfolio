import numpy as np
import random as rd 
import sys
from matplotlib import pyplot as plt
sim=1000
orde2=[[0]*sim for i in range(2)]
d1=0
tfinal=100
Ng=2
delta=0.5
e=0.5
mp=0.025
evec=np.arange(0.5,0.51,0.2)
mvec=np.arange(0,0.1,0.001)
moda=np.zeros((Ng,len(evec),len(mvec)))
d=np.zeros((len(evec),len(mvec)))

for e in evec:
    
    #p1=int((e-evec[0])/(evec[1]-evec[0]))
    p1=0
    for mp in mvec:
        d1=0
        q1=int((mp-mvec[0])/(mvec[1]-mvec[0]))
        print(p1,q1)
        for s in range(sim):
            ###Funcións veciños
            def vi(k):
                if (k>0):x=k-1
                elif (k==0): x=Ng-1 
                return x
            def vd(k):
                if (k<Ng-1):x=k+1
                elif (k==Ng-1): x=0 
                return x
            #############
            x=[np.zeros((2,2)) for i in range(Ng)]
            n=2
            m=2
            x00=[[] for i in range(Ng)]
            x01=[[] for i in range(Ng)]
            x10=[[] for i in range(Ng)]
            x11=[[] for i in range(Ng)]
            np.seterr('raise')
            #Just one group
            def fit(k,i,j):
                w=1+delta*(e*(x[k][i,0]+x[k][i,1])+(1-e)*x[k][i,j]/(x[k][0,j]+x[k][1,j]))
                return w
            p=[rd.uniform(0,1) for i in range(Ng)]
            q=[rd.uniform(0,1) for i in range(Ng)]
            for k in range(Ng):
                x[k][0,0]=p[k]*q[k]
                x[k][0,1]=p[k]*(1-q[k])
                x[k][1,0]=(1-p[k])*q[k]
                x[k][1,1]=(1-p[k])*(1-q[k])
            
            for t in range(tfinal-1):
                ###Migración 
                for k in range(Ng):
                    nd=vd(k)
                    ni=vi(k)
                    for i in range(n):
                        for j in range(m):
                            x[k][i,j]=(1-mp)*x[k][i,j]+mp/2*x[nd][i,j]+mp/2*x[ni][i,j]
                ########Replicator dynamics
                for k in range(Ng):
                    w11=fit(k,1,1)
                    w00=fit(k,0,0)
                    w01=fit(k,0,1)
                    w10=fit(k,1,0)
                    wbar=x[k][0,0]*w00+x[k][1,0]*w10+x[k][0,1]*w01+x[k][1,1]*w11
                    x[k][0,0]=x[k][0,0]*w00/wbar
                    x[k][0,1]=x[k][0,1]*w01/wbar
                    x[k][1,0]=x[k][1,0]*w10/wbar
                    x[k][1,1]=x[k][1,1]*w11/wbar
                    x00[k].append(x[k][0,0])
                    x10[k].append(x[k][1,0])
                    x01[k].append(x[k][0,1])
                    x11[k].append(x[k][1,1])
                    
            #Proba do parámetro de orde 
            orde=[0]*Ng
            primeros=[0]*Ng
            
            for i in range(Ng):
                orde[i]=np.amax(x[i])    
                m1=np.where(x[i]==orde[i])[1][0]
                primeros[i]=np.where(x[i]==orde[i])
                m2=np.where(x[i]==np.partition(x[i].flatten(), -2)[-2])[1][0]        
                if (m1!=m2): orde[i]=orde[i]*(-1)
                orde2[i][s]=orde[i]
            if (primeros[0]!=primeros[1]): d1=d1+1
        #Calculamos os valores de celda
        histo=[0]*Ng
        for i in range(Ng):
            histo[i]=np.histogram(orde2[i],bins=50)
            moda[i,p1,q1]=(histo[i][1][np.argmax(histo[i][0])-1]+histo[i][1][np.argmax(histo[i][0])+1])/2
        d[p1,q1]=d1/sim
        print(d[p1,q1])
fig, ax = plt.subplots()
extent = (0, 0.1, 0, 0.1)
im = ax.imshow(moda[0], cmap=plt.cm.hot, origin='upper', extent=extent)
plt.colorbar(im)